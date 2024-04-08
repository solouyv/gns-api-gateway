import json

from fastapi.responses import Response

from gns_api_gateway.application import GNS3Service
from gns_api_gateway.async_rest_client import Methods, Response as ProxyResponse
from gns_api_gateway.constants import TOKEN_KEY
from gns_api_gateway.infrastructure import GNS3Proxy
from .abstract_router import AbstractRouter, RequestMapper
from ..auth import get_user_token
from ..utilites import ParsedRequest, ResponseBuilder

__all__ = ["GNS3Router"]


class GNS3Router(AbstractRouter):
    def __init__(self, client: GNS3Proxy, service: GNS3Service) -> None:
        super().__init__(client)
        self._service = service

    @property
    def request_mapper(self) -> RequestMapper:
        return {
            (Methods.GET, rf"^/$"): self._set_auth_token,
            (Methods.GET, rf"^/v2/projects$"): self._get_projects,
            (Methods.POST, rf"^/v2/projects$"): self._create_project,
            (Methods.DELETE, rf"^/v2/projects/\d+$"): self._delete_project,
        }

    async def _set_auth_token(self, request: ParsedRequest) -> Response:
        response = await self._client.request(method=Methods.GET, url="/")

        return (
            ResponseBuilder()
            .with_content(response.content)
            .with_status(response.status_code)
            .with_headers(response.headers)
            .with_cookie(key=TOKEN_KEY, value=get_user_token())
            .build()
        )

    async def _get_projects(self, request: ParsedRequest) -> Response:
        response = await self._make_default_request(request)
        projects = response.get_content()
        response.change_content(await self._service.get_user_projects(projects))

        return self._return_default_response(response)

    async def _create_project(self, request: ParsedRequest):
        response = await self._make_default_request(request)
        if response.status_code_ok():
            await self._service.add_project_to_user(response.get_content()["project_id"])

        return self._return_default_response(response)

    async def _delete_project(self, request: ParsedRequest):
        response = await self._make_default_request(request)
        if response.status_code_ok():
            await self._service.remove_project_from_user(response.get_content()["project_id"])

        return self._return_default_response(response)

    async def _make_default_request(self, request: ParsedRequest) -> ProxyResponse:
        return await self._client.request(**await request.to_dict())

    @staticmethod
    def _return_default_response(response: ProxyResponse) -> Response:
        return (
            ResponseBuilder()
            .with_content(response.content)
            .with_status(response.status_code)
            .with_headers(response.headers)
            .build()
        )
