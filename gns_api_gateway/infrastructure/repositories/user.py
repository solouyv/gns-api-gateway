__all__ = ["UserRepository"]

from gns_api_gateway.datasource import Database


class UserRepository:
    def __init__(self, db: Database) -> None:
        self._db = db
