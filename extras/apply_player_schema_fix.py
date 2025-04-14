"""
Script to fix the Player model schema inconsistencies.
Run this script to apply the fixes to the database.
"""
import os
import argparse
from sqlalchemy import create_engine, text

def create_db_url():
    """Create database URL from environment variables or default values."""
    db_user = os.environ.get("DB_USER", "postgres")
    db_password = os.environ.get("DB_PASSWORD", "postgres")
    db_host = os.environ.get("DB_HOST", "localhost")
    db_port = os.environ.get("DB_PORT", "5432")
    db_name = os.environ.get("DB_NAME", "postscore")
    
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

def apply_migrations(sql_file_path):
    """Apply migrations from the SQL file."""
    db_url = create_db_url()
    print(f"Connecting to database at {db_url}")
    
    try:
        # Create engine
        engine = create_engine(db_url)
        
        # Read SQL file
        with open(sql_file_path, 'r') as f:
            sql = f.read()
        
        # Execute SQL within a transaction
        with engine.begin() as conn:
            conn.execute(text(sql))
            
        print("Migration applied successfully!")
        return True
    except Exception as e:
        print(f"Error applying migration: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Apply player schema fix.')
    parser.add_argument('--sql-file', default='migrations/fix_player_model_schema.sql',
                        help='Path to SQL migration file')
    args = parser.parse_args()
    
    if not os.path.exists(args.sql_file):
        print(f"Error: SQL file not found at {args.sql_file}")
        return False
    
    return apply_migrations(args.sql_file)

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 