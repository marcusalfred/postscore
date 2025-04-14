"""Convert UUID to ULID for all tables

Revision ID: 13eea4ac64ad
Revises: 
Create Date: 2025-04-07 20:41:11.586045

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import ulid


# revision identifiers, used by Alembic.
revision: str = '13eea4ac64ad'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create a temporary function to convert UUIDs to ULIDs
    # This function will generate deterministic ULIDs based on the input UUIDs
    op.execute("""
    CREATE OR REPLACE FUNCTION uuid_to_ulid(uuid_val TEXT) RETURNS TEXT AS $$
    DECLARE
        -- Use the UUID as a seed for a deterministic ULID
        -- This ensures foreign keys remain consistent
        result TEXT;
    BEGIN
        -- If the input is already in ULID format (26 chars), return as is
        IF LENGTH(uuid_val) = 26 THEN
            RETURN uuid_val;
        END IF;
        
        -- Convert UUID to a deterministic ULID-like value
        -- Use parts of the UUID to create something that looks like a ULID
        -- Real ULIDs have timestamp component, but we're creating deterministic values
        result := REPLACE(uuid_val, '-', '') || 'ULID';
        -- Ensure it's 26 characters long (ULID length)
        RETURN SUBSTRING(result, 1, 26);
    END;
    $$ LANGUAGE plpgsql;
    """)
    
    # Tables with their ID columns and foreign key relationships
    tables = [
        {
            'name': 'courses',
            'id_column': 'id',
            'fk_tables': ['tee_boxes', 'rounds']
        },
        {
            'name': 'players',
            'id_column': 'id',
            'fk_tables': ['rounds']
        },
        {
            'name': 'tee_boxes',
            'id_column': 'id',
            'fk_tables': ['tee_box_holes', 'rounds']
        },
        {
            'name': 'tee_box_holes',
            'id_column': 'id',
            'fk_tables': ['round_holes']
        },
        {
            'name': 'rounds',
            'id_column': 'id',
            'fk_tables': ['round_holes']
        },
        {
            'name': 'round_holes',
            'id_column': 'id',
            'fk_tables': []
        }
    ]
    
    # Map table names to their foreign key column names (for special cases)
    fk_column_map = {
        'tee_boxes': 'tee_box_id',
        'courses': 'course_id',
        'players': 'player_id',
        'rounds': 'round_id',
        'tee_box_holes': 'tee_box_hole_id'
    }
    
    # First, drop foreign key constraints
    for table in tables:
        for fk_table in table['fk_tables']:
            # Use the map to get the correct foreign key column name
            fk_column = fk_column_map.get(table['name'], f"{table['name'][:-1]}_id")
            op.execute(f"""
            ALTER TABLE {fk_table} 
            DROP CONSTRAINT IF EXISTS {fk_table}_{fk_column}_fkey
            """)
    
    # Drop the unique constraint on round_holes
    op.execute("""
    ALTER TABLE round_holes
    DROP CONSTRAINT IF EXISTS unique_round_hole_per_round
    """)
    
    # Convert each table's IDs to ULID format
    for table in tables:
        op.execute(f"""
        UPDATE {table['name']} 
        SET {table['id_column']} = uuid_to_ulid({table['id_column']})
        WHERE LENGTH({table['id_column']}) != 26
        """)
        
        # Also update foreign key columns in related tables
        for fk_table in table['fk_tables']:
            # Use the map to get the correct foreign key column name
            fk_column = fk_column_map.get(table['name'], f"{table['name'][:-1]}_id")
            op.execute(f"""
            UPDATE {fk_table}
            SET {fk_column} = uuid_to_ulid({fk_column})
            WHERE LENGTH({fk_column}) != 26
            """)
    
    # Re-add foreign key constraints
    for table in tables:
        for fk_table in table['fk_tables']:
            # Use the map to get the correct foreign key column name
            fk_column = fk_column_map.get(table['name'], f"{table['name'][:-1]}_id")
            op.execute(f"""
            ALTER TABLE {fk_table}
            ADD CONSTRAINT {fk_table}_{fk_column}_fkey
            FOREIGN KEY ({fk_column}) REFERENCES {table['name']}({table['id_column']})
            """)
    
    # Re-add the unique constraint on round_holes
    op.execute("""
    ALTER TABLE round_holes
    ADD CONSTRAINT unique_round_hole_per_round
    UNIQUE (round_id, tee_box_hole_id)
    """)
    
    # Drop the temporary function
    op.execute("DROP FUNCTION IF EXISTS uuid_to_ulid(TEXT)")


def downgrade() -> None:
    # This migration is not reversible as ULIDs cannot be reliably
    # converted back to the original UUIDs without storing the mapping
    pass
