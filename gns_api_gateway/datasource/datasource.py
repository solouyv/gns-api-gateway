import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from urllib import parse

import asyncpg
from sqlalchemy import MetaData

from .backoff import async_backoff

__all__ = ["Database", "metadata"]

metadata = MetaData()


class Database:
    def __init__(
        self,
        username: str,
        password: str,
        host: str,
        port: int,
        database: str,
        require_secure_transport: bool = False,
        connection_pool_max_size: int = 10,
        sslkey: str = "",
        sslcert: str = "",
        sslrootcert: str = "",
        sslmode: str = "verify-full",
    ):
        self._username = username
        self._password = password
        self._host = host
        self._port = port
        self._database = database
        self._require_secure_transport = require_secure_transport
        self._connection_pool_max_size = connection_pool_max_size

        self._sslkey = sslkey
        self._sslcert = sslcert
        self._sslrootcert = sslrootcert
        self._sslmode = sslmode

        self._connection_pool = None

        self._logger = logging.getLogger(__name__)

    async def connect(self) -> None:
        await self._initialize_connection_pool()

    async def close(self) -> None:
        await self._close_connection_pool()

    @async_backoff(times=3)
    async def acquire_connection(self) -> asyncpg.Connection:
        if not self._connection_pool:
            await self._initialize_connection_pool()

        connection = await self._connection_pool.acquire()
        await self.check_connection(connection)

        return connection

    async def release_connection(self, connection: asyncpg.Connection) -> None:
        await self._connection_pool.release(connection)

    @asynccontextmanager
    async def connection(self) -> AsyncGenerator:
        connection = await self.acquire_connection()

        try:
            async with connection.transaction():
                yield connection

        finally:
            await self.release_connection(connection)

    async def healthcheck(self) -> None:
        async with self.connection() as conn:
            await conn.execute("select 1;")

    async def check_connection(self, connection: asyncpg.Connection) -> None:
        try:
            await connection.execute("select 1;")

        except Exception as err:
            self._logger.error(f"Connection test failed with error: {err}.")

            await self.release_connection(connection)
            raise

    async def _initialize_connection_pool(self) -> None:
        self._connection_pool = await asyncpg.create_pool(
            dsn=self._dsn,
            max_size=self._connection_pool_max_size,
        )

        self._logger.debug("Connection pool initialized")

    async def _close_connection_pool(self) -> None:
        if self._connection_pool:
            await self._connection_pool.close()
            self._connection_pool = None

        self._logger.debug("Connection pool closed")

    @property
    def _dsn(self) -> str:
        query_params = {
            "sslkey": self._sslkey,
            "sslcert": self._sslcert,
            "sslrootcert": self._sslrootcert,
            "sslmode": self._sslmode if self._require_secure_transport and self._sslmode else None,
        }
        query = parse.urlencode({k: v for k, v in query_params.items() if v})

        dsn = f"postgresql://{self._username}:{self._password}@{self._host}:{self._port}/{self._database}"
        if query:
            dsn = f"{dsn}?{query}"

        return dsn
