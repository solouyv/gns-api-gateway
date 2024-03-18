import abc
import logging
from typing import Any, Optional

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from aiohttp_retry import ExponentialRetry, RetryClient

from .auth_providers import BaseAuthProvider
from .client_utils import CommonDictType, check_arguments
from .constants import Methods

__all__ = ["AbstractRestClient"]


class AbstractRestClient(abc.ABC):
    RETRIED_STATUSES: set[int] = {429, 500, 502, 503, 504}
    RETRY_ATTEMPTS: int = 8

    def __init__(
        self,
        base_url: str,
        *,
        verify_ssl: bool = False,
        timeout: int = 60,
        headers: Optional[CommonDictType] = None,
    ) -> None:
        self._session = ClientSession(
            base_url=base_url,
            connector=TCPConnector(verify_ssl=verify_ssl),
            timeout=ClientTimeout(total=timeout),
        )
        self._session_headers = headers
        self._logger = logging.getLogger(self.__class__.__name__)
        self._initialize()

    @check_arguments
    async def request(self, *, method: Methods, url: str, **kwargs) -> dict[str, Any]:
        headers = self._unify_headers(kwargs)
        async with self._client.request(
            method=method,
            url=url,
            headers=headers,
            **kwargs,
        ) as response:
            return {
                "content": await response.read(),
                "status_code": response.status,
                "headers": response.headers,
            }

    async def close(self) -> None:
        await self._client.close()
        await self._session.close()

    def _initialize(self) -> None:
        self._create_client()
        self._set_session_headers()
        self._set_authentication()

    def _create_client(self) -> None:
        self._client = RetryClient(
            client_session=self._session,
            retry_options=ExponentialRetry(
                attempts=self.RETRY_ATTEMPTS,
                retry_all_server_errors=False,
                statuses=self.RETRIED_STATUSES,
            ),
            logger=self._logger,
        )

    def _set_session_headers(self) -> None:
        if self._session_headers is not None:
            self._session.headers.update(self._session_headers)

    def _set_authentication(self) -> None:
        self._auth_provider = BaseAuthProvider()

    def _unify_headers(self, kwargs: CommonDictType) -> CommonDictType:
        headers = self._auth_provider.make_headers()
        if "headers" in kwargs:
            kwargs_headers = kwargs.pop("headers")
            headers.update(kwargs_headers)
        return headers
