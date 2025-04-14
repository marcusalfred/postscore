"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from ulid import ULID
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '${up_revision}'
down_revision = '${down_revision}'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Migration upgrade operations.
    
    Add detailed comments explaining the purpose of each operation.
    Group related operations together.
    Include seed data if necessary.
    """
    # Example: Create a new table
    # op.create_table(
    #     'example_table',
    #     sa.Column('id', sa.String(26), primary_key=True, default=str(ULID())),
    #     sa.Column('name', sa.String(100), nullable=False),
    #     sa.Column('description', sa.Text),
    #     sa.Column('created_on', sa.DateTime, nullable=False, server_default=sa.func.now()),
    # )
    
    # Example: Add column to existing table
    # op.add_column('existing_table', sa.Column('new_column', sa.String(50)))
    
    # Example: Create index
    # op.create_index('ix_example_name', 'example_table', ['name'])
    
    # Example: Seed data
    # op.bulk_insert(
    #     sa.table(
    #         'example_table',
    #         sa.Column('id', sa.String(26)),
    #         sa.Column('name', sa.String(100)),
    #         sa.Column('description', sa.Text),
    #     ),
    #     [
    #         {'id': str(ULID()), 'name': 'Example 1', 'description': 'Description 1'},
    #         {'id': str(ULID()), 'name': 'Example 2', 'description': 'Description 2'},
    #     ]
    # )
    pass


def downgrade() -> None:
    """
    Migration downgrade operations.
    
    Implement in reverse order of the upgrade operations.
    Be careful with destructive operations that might lose data.
    """
    # Example: Drop table
    # op.drop_table('example_table')
    
    # Example: Drop column
    # op.drop_column('existing_table', 'new_column')
    
    # Example: Drop index
    # op.drop_index('ix_example_name', 'example_table')
    pass 