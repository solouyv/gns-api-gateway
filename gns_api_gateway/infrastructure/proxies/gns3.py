import json
from http import HTTPStatus
from typing import Any

from gns_api_gateway.async_rest_client import Methods
from .generic_rest_client import GenericRestClient
from ...domain.exceptions import GNS3ProxyError

__all__ = ["GNS3Proxy"]


class GNS3Proxy(GenericRestClient):
    async def get_document_types(
        self, method: Methods, url: str, query: str, headers: dict[str, Any], data: bytes
    ) -> dict:
        response = await self.request(method, url, query, headers, data)

        if response["status_code"] != HTTPStatus.OK:
            raise GNS3ProxyError("Can't get document types!")

        return json.loads(response["content"])
