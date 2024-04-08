from sqlalchemy import Column, String, Table, Integer, JSON

from gns_api_gateway.datasource import metadata

__all__ = ["user_table"]

user_table = Table(
    "users_user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(150), nullable=False, unique=True),
    Column("first_name", String(150), nullable=False),
    Column("last_name", String(150), nullable=False),
    Column("role", Integer, nullable=False),
    Column("projects", JSON, nullable=False),
)
