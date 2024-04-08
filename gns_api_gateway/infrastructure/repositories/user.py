from gns_api_gateway.datasource import Database
from gns_api_gateway.domain import User
from gns_api_gateway.infrastructure.tables import token_table
from gns_api_gateway.infrastructure.tables.user import user_table

__all__ = ["UserRepository"]


class UserRepository:
    def __init__(self, db: Database) -> None:
        self._db = db
        self._user_table = user_table
        self._token_table = token_table

    async def get_user_by_token(self, token: str) -> User:
        async with self._db.connection() as conn:
            res = await conn.fetchrow(
                f"select * from {self._user_table} left outer join {self._token_table} "
                f"on {self._user_table.c.id}={self._token_table.c.user_id} "
                f"where {self._token_table.c.key}='{token}';",
            )

            return User.from_dict(dict(res))

    async def update(self, user: User) -> None:
        async with self._db.connection() as conn:
            query = f"update {self._user_table} set {user.to_query()} where {self._user_table.c.id}={user.id};"
            await conn.execute(query)
