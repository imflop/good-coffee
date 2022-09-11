"""Init revision

Revision ID: 9fd2940fc8e9
Revises: 
Create Date: 2022-09-11 20:54:49.292300

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9fd2940fc8e9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "countries",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=512), nullable=False),
        sa.Column("slug_name", sa.String(length=1024), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name")
    )
    op.create_table(
        "cities",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=512), nullable=False),
        sa.Column("slug_name", sa.String(length=1024), nullable=False),
        sa.Column("country_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_table(
        "coffee_shops",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=512), nullable=False),
        sa.Column("slug_name", sa.String(length=1024), nullable=False),
        sa.Column("instagram_url", sa.String(length=512), nullable=False),
        sa.Column("city_id", sa.Integer(), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("description", sa.String(length=1024), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("timezone('UTC'::text, now())"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("timezone('UTC'::text, now())"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("countries")
    op.drop_table("cities")
    op.drop_table("coffee_shops")
