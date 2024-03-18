import json
from typing import Any, Union

from fastapi import Request
from starlette.datastructures import Headers

from gns_api_gateway.async_rest_client import Methods

__all__ = ["ParsedRequest"]


class ParsedRequest:
    def __init__(self, request: Request) -> None:
        self._request = request
        self.url = request.url.path
        self.headers = request.headers

    @property
    def method(self) -> Methods:
        return Methods(self._request.method)

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str) -> None:
        self._url = url

    @property
    async def form(self) -> dict[str, Any]:
        form_data = await self._request.form()
        return {key: value for key, value in form_data.items()}

    @property
    def headers(self) -> dict[str, Any]:
        return self._headers

    @headers.setter
    def headers(self, headers: Union[Headers, dict[str, Any]]) -> None:
        if isinstance(headers, Headers):
            self._headers = dict(headers)
        else:
            self._headers = headers

    @property
    async def json_data(self) -> dict[str, Any]:
        return json.loads(await self._request.body())

    def add_element_in_headers(self, element: dict[str, Any]) -> None:
        self.headers.update(element)

    def change_url(self, current_prefix: str, new_prefix: str) -> "ParsedRequest":
        self.url = self.url.replace(current_prefix, new_prefix)
        return self

    async def change_body(self, new_body: bytes) -> None:
        async def receive() -> dict[str, Any]:  # noqa: WPS430
            return {"type": "http.request", "body": new_body, "more_body": False}

        self._request = Request(self._request.scope.copy(), receive=receive)

    async def to_dict(self) -> dict[str, Any]:
        url = self.url
        if self._request.url.query:
            url = "?".join((self.url, self._request.url.query))

        return {
            "method": self.method,
            "url": url,
            "headers": self.headers,
            "data": await self._request.body(),
        }
