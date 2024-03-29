"""migration 1

Revision ID: fe9ecc0f09d7
Revises: 
Create Date: 2023-03-13 23:34:38.010047

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fe9ecc0f09d7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('login_history_2022')
    op.drop_table('login_history_2023')
    op.create_unique_constraint(None, 'login_history', ['id', 'create_at'])
    op.create_unique_constraint(None, 'permission', ['id'])
    op.create_unique_constraint(None, 'role', ['id'])
    op.create_unique_constraint(None, 'role_permission_relation', ['id'])
    op.create_unique_constraint(None, 'user', ['id'])
    op.create_unique_constraint(None, 'user_role_relation', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_role_relation', type_='unique')
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'role_permission_relation', type_='unique')
    op.drop_constraint(None, 'role', type_='unique')
    op.drop_constraint(None, 'permission', type_='unique')
    op.drop_constraint(None, 'login_history', type_='unique')
    op.create_table('login_history_2023',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('create_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='login_history_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', 'create_at', name='login_history_2023_pkey')
    )
    op.create_table('login_history_2022',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('create_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='login_history_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', 'create_at', name='login_history_2022_pkey')
    )
    # ### end Alembic commands ###
