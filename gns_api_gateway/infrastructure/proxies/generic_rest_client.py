from http import HTTPStatus
from typing import Any

from gns_api_gateway.async_rest_client import AbstractRestClient, AsyncRestClientError, TokenAuthProvider
from gns_api_gateway.infrastructure import user

__all__ = ["GenericRestClient"]


class GenericRestClient(AbstractRestClient):
    exception: type[AsyncRestClientError]

    def _set_authentication(self) -> None:
        self._auth_provider = TokenAuthProvider(user)

    def _check_response(self, response: dict[str, Any], url: str) -> None:
        response_status_code = response["status_code"]
        response_content = response["content"]
        if response_status_code >= HTTPStatus.BAD_REQUEST:
            self._logger.error(
                "Response for url `%s` with status code `%s` failed with error %s",
                url,
                response_status_code,
                response_content,
            )

            raise self.exception(response_content)
