from fastapi.responses import Response

from gns_api_gateway.async_rest_client import Methods
from gns_api_gateway.constants import TOKEN_KEY
from gns_api_gateway.infrastructure import GNS3Proxy
from .abstract_router import AbstractRouter, RequestMapper
from ..auth import get_user_token
from ..utilites import ParsedRequest, ResponseBuilder

__all__ = ["GNS3Router"]


class GNS3Router(AbstractRouter):
    def __init__(self, client: GNS3Proxy) -> None:
        super().__init__(client)

    @property
    def request_mapper(self) -> RequestMapper:
        return {
            (Methods.GET, rf"^/$"): self._open_projects,
        }

    async def _open_projects(self, request: ParsedRequest) -> Response:
        response = await self._client.request(method=Methods.GET, url="/")
        return (
            ResponseBuilder()
            .with_content(response["content"])
            .with_status(response["status_code"])
            .with_headers(response["headers"])
            .with_cookie(key=TOKEN_KEY, value=get_user_token())
            .build()
        )
