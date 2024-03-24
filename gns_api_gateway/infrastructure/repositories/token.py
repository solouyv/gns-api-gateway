from gns_api_gateway.datasource import Database
from gns_api_gateway.infrastructure.tables import token_table

__all__ = ["TokenRepository"]


class TokenRepository:
    def __init__(self, db: Database) -> None:
        self._db = db

    async def get_tokens(self) -> set[str]:
        async with self._db.connection() as conn:
            res = await conn.fetch(f"select {token_table.c.key} from {token_table}")

            return {r[0] for r in res}
