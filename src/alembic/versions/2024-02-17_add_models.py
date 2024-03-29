"""add models

Revision ID: 8f877abab01f
Revises:
Create Date: 2024-02-17 00:25:38.954376

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import geoalchemy2

# revision identifiers, used by Alembic.
revision: str = "8f877abab01f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "business",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "location",
            geoalchemy2.types.Geography(
                geometry_type="POINT",
                srid=4326,
                from_text="ST_GeogFromText",
                name="geography",
                nullable=False,
            ),
            nullable=False,
        ),
        sa.Column("address_line1", sa.String(length=255), nullable=False),
        sa.Column("address_line2", sa.String(length=255), nullable=False),
        sa.Column("ar_name", sa.String(length=255), nullable=False),
        sa.Column("city", sa.String(length=255), nullable=False),
        sa.Column("country", sa.String(length=255), nullable=False),
        sa.Column("en_name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=255), nullable=False),
        sa.Column("type", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    # op.create_index(
    #     "idx_business_location",
    #     "business",
    #     ["location"],
    #     unique=False,
    #     postgresql_using="gist",
    # )
    op.create_table(
        "category",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("ar_name", sa.String(length=255), nullable=False),
        sa.Column("en_name", sa.String(length=255), nullable=False),
        sa.Column("parent_id", sa.UUID(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["category.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_table(
        "features_category",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("ar_name", sa.String(length=255), nullable=False),
        sa.Column("en_name", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "business_categories",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("business_id", sa.UUID(), nullable=False),
        sa.Column("category_id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["business_id"], ["business.id"], initially="DEFERRED", deferrable=True
        ),
        sa.ForeignKeyConstraint(
            ["category_id"], ["category.id"], initially="DEFERRED", deferrable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "business_categories_business_id_index",
        "business_categories",
        ["business_id"],
        unique=False,
    )
    op.create_index(
        "business_categories_category_id_index",
        "business_categories",
        ["category_id"],
        unique=False,
    )
    op.create_table(
        "business_contacts",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("contact_type", sa.String(length=15), nullable=False),
        sa.Column("contact_value", sa.String(length=255), nullable=False),
        sa.Column("business_id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["business_id"], ["business.id"], initially="DEFERRED", deferrable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "business_contacts_business_id_index",
        "business_contacts",
        ["business_id"],
        unique=False,
    )
    op.create_table(
        "business_tags",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("tag", sa.String(length=255), nullable=False),
        sa.Column("business_id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["business_id"], ["business.id"], initially="DEFERRED", deferrable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "business_tags_business_id_index",
        "business_tags",
        ["business_id"],
        unique=False,
    )
    op.create_table(
        "business_working_hours",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("day", sa.Integer(), nullable=False),
        sa.Column("opening_time", sa.Time(), nullable=False),
        sa.Column("closing_time", sa.Time(), nullable=False),
        sa.Column("business_id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["business_id"], ["business.id"], initially="DEFERRED", deferrable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "business_working_hours_business_id_day_index",
        "business_working_hours",
        ["business_id", "day"],
        unique=False,
    )
    op.create_table(
        "feature",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("ar_name", sa.String(length=255), nullable=False),
        sa.Column("en_name", sa.String(length=255), nullable=False),
        sa.Column("category_id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"], ["category.id"], initially="DEFERRED", deferrable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "business_features",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("business_id", sa.UUID(), nullable=False),
        sa.Column("feature_id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["business_id"], ["business.id"], initially="DEFERRED", deferrable=True
        ),
        sa.ForeignKeyConstraint(
            ["feature_id"], ["feature.id"], initially="DEFERRED", deferrable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "business_features_business_id_index",
        "business_features",
        ["business_id"],
        unique=False,
    )
    op.create_index(
        "business_features_feature_id_index",
        "business_features",
        ["feature_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("business_features_feature_id_index", table_name="business_features")
    op.drop_index("business_features_business_id_index", table_name="business_features")
    op.drop_table("business_features")
    op.drop_table("feature")
    op.drop_index(
        "business_working_hours_business_id_day_index",
        table_name="business_working_hours",
    )
    op.drop_table("business_working_hours")
    op.drop_index("business_tags_business_id_index", table_name="business_tags")
    op.drop_table("business_tags")
    op.drop_index("business_contacts_business_id_index", table_name="business_contacts")
    op.drop_table("business_contacts")
    op.drop_index(
        "business_categories_category_id_index", table_name="business_categories"
    )
    op.drop_index(
        "business_categories_business_id_index", table_name="business_categories"
    )
    op.drop_table("business_categories")
    op.drop_table("features_category")
    op.drop_table("category")
    op.drop_index(
        "idx_business_location", table_name="business", postgresql_using="gist"
    )
    op.drop_table("business")
    # ### end Alembic commands ###
