"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-03-24
"""
import sqlalchemy as sa
from alembic import op

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'players',
        sa.Column('id', sa.String(26), primary_key=True, nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('email', sa.String(50), nullable=True, unique=True),
        sa.Column('zip', sa.String(50), nullable=True),
        sa.Column('handicap', sa.Float(), nullable=True),
        sa.Column('ghin_number', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('hashed_password', sa.String(128), nullable=True),
        sa.Column('is_super', sa.Boolean(), server_default='false'),
        sa.Column('created_on', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
    )
    op.create_index('idx_players_email', 'players', ['email'])

    op.create_table(
        'courses',
        sa.Column('id', sa.String(26), primary_key=True, nullable=False),
        sa.Column('name', sa.String(50), nullable=False, unique=True),
        sa.Column('address', sa.String(50), nullable=True),
        sa.Column('city', sa.String(50), nullable=True),
        sa.Column('state', sa.String(50), nullable=True),
        sa.Column('zip', sa.String(50), nullable=True),
        sa.Column('website', sa.String(50), nullable=True),
        sa.Column('created_on', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
    )
    op.create_index('idx_courses_name', 'courses', ['name'])

    op.create_table(
        'tee_boxes',
        sa.Column('id', sa.String(26), primary_key=True, nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('course_id', sa.String(26), sa.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False),
        sa.Column('rating', sa.Float(), nullable=True),
        sa.Column('slope', sa.Integer(), nullable=True),
        sa.Column('yardage', sa.Integer(), nullable=True),
        sa.Column('hex', sa.String(50), nullable=True),
        sa.Column('created_on', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.UniqueConstraint('course_id', 'name', name='uq_tee_box_course_name'),
    )
    op.create_index('idx_tee_boxes_course_id', 'tee_boxes', ['course_id'])

    op.create_table(
        'tee_box_holes',
        sa.Column('id', sa.String(26), primary_key=True, nullable=False),
        sa.Column('tee_box_id', sa.String(26), sa.ForeignKey('tee_boxes.id', ondelete='CASCADE'), nullable=False),
        sa.Column('hole_number', sa.Integer(), nullable=True),
        sa.Column('par', sa.Integer(), nullable=True),
        sa.Column('yardage', sa.Integer(), nullable=True),
        sa.Column('handicap', sa.Integer(), nullable=True),
        sa.Column('created_on', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
    )
    op.create_index('idx_tee_box_holes_tee_box_id', 'tee_box_holes', ['tee_box_id'])

    op.create_table(
        'rounds',
        sa.Column('id', sa.String(26), primary_key=True, nullable=False),
        sa.Column('course_id', sa.String(26), sa.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False),
        sa.Column('tee_box_id', sa.String(26), sa.ForeignKey('tee_boxes.id', ondelete='CASCADE'), nullable=False),
        sa.Column('player_id', sa.String(26), sa.ForeignKey('players.id', ondelete='CASCADE'), nullable=False),
        sa.Column('total_score', sa.Integer(), nullable=True),
        sa.Column('holes', sa.Integer(), nullable=True),
        sa.Column('start_time', sa.DateTime(), nullable=True),
        sa.Column('end_time', sa.DateTime(), nullable=True),
        sa.Column('created_on', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
    )
    op.create_index('idx_rounds_player_id', 'rounds', ['player_id'])
    op.create_index('idx_rounds_course_id', 'rounds', ['course_id'])

    op.create_table(
        'round_holes',
        sa.Column('id', sa.String(26), primary_key=True, nullable=False),
        sa.Column('round_id', sa.String(26), sa.ForeignKey('rounds.id', ondelete='CASCADE'), nullable=False),
        sa.Column('tee_box_hole_id', sa.String(26), sa.ForeignKey('tee_box_holes.id', ondelete='CASCADE'), nullable=False),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('gir', sa.Boolean(), nullable=True),
        sa.Column('fairway', sa.String(), nullable=True),
        sa.Column('putts', sa.Integer(), nullable=True),
        sa.Column('penalties', sa.Integer(), nullable=True),
        sa.Column('sand', sa.Boolean(), nullable=True),
        sa.Column('water', sa.Boolean(), nullable=True),
        sa.Column('created_on', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.UniqueConstraint('round_id', 'tee_box_hole_id', name='unique_round_hole_per_round'),
    )
    op.create_index('idx_round_holes_round_id', 'round_holes', ['round_id'])


def downgrade() -> None:
    op.drop_table('round_holes')
    op.drop_table('rounds')
    op.drop_table('tee_box_holes')
    op.drop_table('tee_boxes')
    op.drop_table('courses')
    op.drop_table('players')
