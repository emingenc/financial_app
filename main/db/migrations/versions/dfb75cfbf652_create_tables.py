"""Create tables

Revision ID: dfb75cfbf652
Revises:
Create Date: 2022-04-12 15:21:50.014228

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "dfb75cfbf652"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("disabled", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=False)
    op.create_table("financial_record", 
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("segment", sa.String(), nullable=True),
        sa.Column("country", sa.String(), nullable=True),
        sa.Column("product", sa.String(), nullable=True),
        sa.Column("discount_band", sa.String(), nullable=True),
        sa.Column("units_sold", sa.Float(), nullable=True),
        sa.Column("manufacturing_price", sa.Float(), nullable=True),
        sa.Column("sale_price", sa.Float(), nullable=True),
        sa.Column("gross_sales", sa.Float(), nullable=True),
        sa.Column("discounts", sa.Float(), nullable=True),
        sa.Column("sales", sa.Float(), nullable=True),
        sa.Column("cogs", sa.Float(), nullable=True),
        sa.Column("profit", sa.Float(), nullable=True),
        sa.Column("currency", sa.String(), nullable=True),
        sa.Column("date", sa.Date(), nullable=True),
        sa.Column("month_number", sa.Integer(), nullable=True),
        sa.Column("month_name", sa.String(), nullable=True),
        sa.Column("year", sa.Integer(), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["owner_id"], ["user.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_financial_record_id"), "financial_record", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_financial_record_id"), table_name="financial_record")
    op.drop_table("financial_record")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_table("user")
    # ### end Alembic commands ###
