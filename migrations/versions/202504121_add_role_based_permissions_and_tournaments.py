"""add_role_based_permissions_and_tournaments

Revision ID: 202504121
Revises: 13eea4ac64ad
Create Date: 2025-04-12

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import ulid
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '202504121'
down_revision = '13eea4ac64ad'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create roles table
    op.create_table('roles',
        sa.Column('id', sa.String(26), primary_key=True),
        sa.Column('name', sa.String(50), nullable=False, unique=True),
        sa.Column('description', sa.String(255)),
    )
    
    # Create permissions table
    op.create_table('permissions',
        sa.Column('id', sa.String(26), primary_key=True),
        sa.Column('name', sa.String(50), nullable=False, unique=True),
        sa.Column('description', sa.String(255)),
    )
    
    # Create role_permissions table (many-to-many)
    op.create_table('role_permissions',
        sa.Column('role_id', sa.String(26), sa.ForeignKey('roles.id'), primary_key=True),
        sa.Column('permission_id', sa.String(26), sa.ForeignKey('permissions.id'), primary_key=True),
    )
    
    # Create player_roles table (many-to-many with context)
    op.create_table('player_roles',
        sa.Column('player_id', sa.String(26), sa.ForeignKey('players.id'), primary_key=True),
        sa.Column('role_id', sa.String(26), sa.ForeignKey('roles.id'), primary_key=True),
        sa.Column('context_id', sa.String(26), nullable=True),  # For tournament-specific roles
        sa.Column('created_on', sa.DateTime, nullable=False, server_default=sa.func.now()),
    )
    
    # Create tournaments table
    op.create_table('tournaments',
        sa.Column('id', sa.String(26), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.String(500)),
        sa.Column('start_date', sa.DateTime, nullable=False),
        sa.Column('end_date', sa.DateTime, nullable=False),
        sa.Column('course_id', sa.String(26), sa.ForeignKey('courses.id'), nullable=False),
        sa.Column('format', sa.String(50)),  # stroke play, match play, stableford, etc.
        sa.Column('status', sa.String(20), server_default='upcoming'),  # upcoming, active, completed
        sa.Column('created_by', sa.String(26), sa.ForeignKey('players.id'), nullable=False),
        sa.Column('created_on', sa.DateTime, nullable=False, server_default=sa.func.now()),
    )
    
    # Create tournament_registrations table
    op.create_table('tournament_registrations',
        sa.Column('id', sa.String(26), primary_key=True),
        sa.Column('tournament_id', sa.String(26), sa.ForeignKey('tournaments.id'), nullable=False),
        sa.Column('player_id', sa.String(26), sa.ForeignKey('players.id'), nullable=False),
        sa.Column('status', sa.String(20), server_default='registered'),  # registered, confirmed, withdrawn
        sa.Column('created_on', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint('tournament_id', 'player_id', name='unique_tournament_player'),
    )
    
    # Create tournament_leaderboard table
    op.create_table('tournament_leaderboard',
        sa.Column('id', sa.String(26), primary_key=True),
        sa.Column('tournament_id', sa.String(26), sa.ForeignKey('tournaments.id'), nullable=False),
        sa.Column('player_id', sa.String(26), sa.ForeignKey('players.id'), nullable=False),
        sa.Column('round_id', sa.String(26), sa.ForeignKey('rounds.id'), nullable=True),
        sa.Column('day', sa.Integer, nullable=False),
        sa.Column('score', sa.Integer, nullable=False),
        sa.Column('total_score', sa.Integer, nullable=False),
        sa.Column('created_on', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint('tournament_id', 'player_id', 'day', name='unique_tournament_player_day'),
    )
    
    # Insert predefined roles
    roles_data = [
        {'id': str(ulid.ULID()), 'name': 'tournament_admin', 'description': 'Full tournament management privileges'},
        {'id': str(ulid.ULID()), 'name': 'tournament_scorer', 'description': 'Can record and view tournament scores'},
        {'id': str(ulid.ULID()), 'name': 'tournament_coordinator', 'description': 'Can manage player registrations and flights'},
    ]
    
    op.bulk_insert(sa.table('roles', 
        sa.Column('id', sa.String(26)),
        sa.Column('name', sa.String(50)),
        sa.Column('description', sa.String(255)),
    ), roles_data)
    
    # Insert predefined permissions
    permissions_data = [
        {'id': str(ulid.ULID()), 'name': 'tournament:create', 'description': 'Can create tournaments'},
        {'id': str(ulid.ULID()), 'name': 'tournament:view', 'description': 'Can view tournament details'},
        {'id': str(ulid.ULID()), 'name': 'tournament:update', 'description': 'Can update tournament details'},
        {'id': str(ulid.ULID()), 'name': 'tournament:delete', 'description': 'Can delete tournaments'},
        {'id': str(ulid.ULID()), 'name': 'tournament:register_players', 'description': 'Can register players for tournaments'},
        {'id': str(ulid.ULID()), 'name': 'tournament:record_scores', 'description': 'Can record and edit tournament scores'},
        {'id': str(ulid.ULID()), 'name': 'tournament:manage_flights', 'description': 'Can organize tournament flights'},
    ]
    
    op.bulk_insert(sa.table('permissions', 
        sa.Column('id', sa.String(26)),
        sa.Column('name', sa.String(50)),
        sa.Column('description', sa.String(255)),
    ), permissions_data)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('tournament_leaderboard')
    op.drop_table('tournament_registrations')
    op.drop_table('tournaments')
    op.drop_table('player_roles')
    op.drop_table('role_permissions')
    op.drop_table('permissions')
    op.drop_table('roles') 