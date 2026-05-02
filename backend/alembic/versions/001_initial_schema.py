"""Initial schema

Revision ID: 001_initial_schema
Revises:
Create Date: 2024-01-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = "001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── service_points ────────────────────────────────────────────────────────
    op.create_table(
        "service_points",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column(
            "type",
            sa.Enum("service_representative", "subcon", "pic_lokasi", name="servicepointtype"),
            nullable=False,
        ),
        sa.Column("city", sa.String(100), nullable=False),
        sa.Column("province", sa.String(100), nullable=False),
        sa.Column("pic_name", sa.String(255), nullable=False),
        sa.Column("pic_phone", sa.String(20), nullable=False),
        sa.Column("pic_email", sa.String(255), nullable=True),
        sa.Column("is_active", sa.Boolean(), default=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    # ── users ─────────────────────────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column(
            "role",
            sa.Enum("admin_jakarta", "user_sp", name="userrole"),
            nullable=False,
        ),
        sa.Column(
            "service_point_id",
            sa.Integer(),
            sa.ForeignKey("service_points.id"),
            nullable=True,
        ),
        sa.Column("is_active", sa.Boolean(), default=True, nullable=False),
        sa.Column("force_password_change", sa.Boolean(), default=False, nullable=False),
        sa.Column("last_login", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    # ── refresh_tokens ────────────────────────────────────────────────────────
    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("token_hash", sa.String(64), unique=True, nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("revoked", sa.Boolean(), default=False, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_refresh_tokens_token_hash", "refresh_tokens", ["token_hash"], unique=True)

    # ── item_types ────────────────────────────────────────────────────────────
    op.create_table(
        "item_types",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean(), default=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    # ── item_categories ───────────────────────────────────────────────────────
    op.create_table(
        "item_categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "type_id", sa.Integer(), sa.ForeignKey("item_types.id"), nullable=False
        ),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean(), default=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    # ── spare_items ───────────────────────────────────────────────────────────
    op.create_table(
        "spare_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("sku", sa.String(100), unique=True, nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column(
            "type_id", sa.Integer(), sa.ForeignKey("item_types.id"), nullable=False
        ),
        sa.Column(
            "category_id",
            sa.Integer(),
            sa.ForeignKey("item_categories.id"),
            nullable=False,
        ),
        sa.Column("unit", sa.String(50), nullable=False),
        sa.Column("requires_serial", sa.Boolean(), default=False, nullable=False),
        sa.Column("min_stock", sa.Integer(), default=0, nullable=False),
        sa.Column("catatan", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), default=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_spare_items_sku", "spare_items", ["sku"], unique=True)

    # ── stock ─────────────────────────────────────────────────────────────────
    op.create_table(
        "stock",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "service_point_id",
            sa.Integer(),
            sa.ForeignKey("service_points.id"),
            nullable=False,
        ),
        sa.Column(
            "spare_item_id",
            sa.Integer(),
            sa.ForeignKey("spare_items.id"),
            nullable=False,
        ),
        sa.Column("qty", sa.Integer(), default=0, nullable=False),
        sa.Column(
            "updated_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=True
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint(
            "service_point_id", "spare_item_id", name="uq_stock_sp_item"
        ),
    )


def downgrade() -> None:
    op.drop_table("stock")
    op.drop_table("spare_items")
    op.drop_table("item_categories")
    op.drop_table("item_types")
    op.drop_table("refresh_tokens")
    op.drop_table("users")
    op.drop_table("service_points")
    op.execute("DROP TYPE IF EXISTS userrole")
    op.execute("DROP TYPE IF EXISTS servicepointtype")
