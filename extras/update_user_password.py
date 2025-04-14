"""
Script to update an existing user's password.
This fixes authentication issues due to incorrectly stored password hashes.
"""
import os
import argparse
from sqlalchemy import create_engine, text
from passlib.context import CryptContext

# Password hashing with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hash a password for storing."""
    return pwd_context.hash(password)

def create_db_url():
    """Create database URL from environment variables or default values."""
    db_user = os.environ.get("DB_USER", "postgres")
    db_password = os.environ.get("DB_PASSWORD", "postgres")
    db_host = os.environ.get("DB_HOST", "localhost")
    db_port = os.environ.get("DB_PORT", "5432")
    db_name = os.environ.get("DB_NAME", "postscore")
    
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

def update_user_password(email, password, make_super=False):
    """Update an existing user's password."""
    db_url = create_db_url()
    print(f"Connecting to database at {db_url}")
    
    try:
        # Create engine
        engine = create_engine(db_url)
        hashed_password = get_password_hash(password)
        
        # First check if the user exists
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT id FROM players WHERE email = :email"),
                {"email": email}
            )
            row = result.fetchone()
            
            if not row:
                print(f"User with email {email} not found")
                return False
            
            user_id = row[0]
            print(f"Found user with ID: {user_id}")
            
        # Update the user's password
        with engine.begin() as conn:
            if make_super:
                conn.execute(
                    text("UPDATE players SET hashed_password = :hashed_password, is_super = TRUE WHERE id = :id"),
                    {"hashed_password": hashed_password, "id": user_id}
                )
                print("User updated and granted superuser privileges")
            else:
                conn.execute(
                    text("UPDATE players SET hashed_password = :hashed_password WHERE id = :id"),
                    {"hashed_password": hashed_password, "id": user_id}
                )
                print("User password updated")
                
        return True
            
    except Exception as e:
        print(f"Error updating user: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Update a user password.')
    parser.add_argument('--email', default='admin@example.com',
                        help='User email')
    parser.add_argument('--password', default='adminpassword',
                        help='New password')
    parser.add_argument('--super', action='store_true',
                        help='Make the user a superuser')
    args = parser.parse_args()
    
    return update_user_password(args.email, args.password, args.super)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 