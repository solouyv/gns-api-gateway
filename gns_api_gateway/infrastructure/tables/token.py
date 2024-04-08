from sqlalchemy import Column, ForeignKey, String, Table, Integer

from gns_api_gateway.datasource import metadata

__all__ = ["token_table"]

token_table = Table(
    "authtoken_token",
    metadata,
    Column("key", String, primary_key=True),
    Column("user_id", Integer, ForeignKey("users_user.id", ondelete="cascade"), nullable=False),
)
