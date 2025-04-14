"""
Script to list all players in the database.
"""
import os
import psycopg2
import psycopg2.extras

def create_db_connection():
    """Create a connection to the database."""
    db_user = os.environ.get("DB_USER", "postgres")
    db_password = os.environ.get("DB_PASSWORD", "postgres")
    db_host = os.environ.get("DB_HOST", "localhost")
    db_port = os.environ.get("DB_PORT", "5432")
    db_name = os.environ.get("DB_NAME", "postscore")
    
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )
    return conn

def list_players():
    """List all players in the database."""
    try:
        conn = create_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Query all players
        cur.execute("""
        SELECT id, name, email, zip, handicap, ghin_number, is_active, is_super
        FROM players
        """)
        
        rows = cur.fetchall()
        if not rows:
            print("No players found in the database")
            return
        
        print(f"Found {len(rows)} players:")
        for row in rows:
            print(f"ID: {row['id']}")
            print(f"  Name: {row['name']}")
            print(f"  Email: {row['email']}")
            print(f"  Active: {row['is_active']}")
            print(f"  Super: {row['is_super']}")
            print(f"  Handicap: {row['handicap']}")
            print("  " + "-" * 40)
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")

if __name__ == "__main__":
    list_players() 