import asyncio
from typing import Any

from gns_api_gateway.async_rest_client import Methods

from gns_api_gateway.constants import GNS3_BASE_API_PREFIX, V1_PREFIX
from gns_api_gateway.infrastructure import GNS3Proxy

__all__ = ["GNS3Service"]



class GNS3Service:
    def __init__(self, gns3_proxy: GNS3Proxy) -> None:
        self._gns3_proxy = gns3_proxy

    # async def find_layouts(self, prototype_id: str) -> dict[str, Any]:
    #     return await self._gns3_proxy.find_layouts(prototype_id)

    # async def find_layout(self, prototype_id: str, reference_layout_id: str, gns_token: str) -> dict[str, Any]:
    #     prototype_task = self._prototype_proxy.find_layout(prototype_id=prototype_id, layout_id=reference_layout_id)
    #     unifier_task = self._unifier_proxy.get_unified_data(
    #         method=Methods.GET,
    #         url=f"{GNS3_BASE_API_PREFIX}{V1_PREFIX}/unified_data/{reference_layout_id}",
    #         query="",
    #         headers={"gns-token": gns_token},
    #         data=b"",
    #     )
    #     parsing_task = self._parsing_proxy.find_document_layout(layout_id=reference_layout_id)
    #
    #     prototype_task_result, unifier_task_result, parsing_task_result = await asyncio.gather(
    #         asyncio.create_task(prototype_task),
    #         asyncio.create_task(unifier_task),
    #         asyncio.create_task(parsing_task),
    #         return_exceptions=True,
    #     )
    #     return ReferenceLayoutResponse(prototype_task_result, unifier_task_result, parsing_task_result).make_response()

    # async def delete_layout(self, prototype_id: str, layout_id: str) -> None:
    #     await self._gns3_proxy.delete_layout(prototype_id=prototype_id, layout_id=layout_id)
    #
    # async def delete_layouts(self, prototype_id: str, layout_ids: list[str]) -> None:
    #     await self._gns3_proxy.delete_layouts(prototype_id=prototype_id, layout_ids=layout_ids)
    def open_projects(self):
        pass
