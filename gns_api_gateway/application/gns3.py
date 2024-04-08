from typing import Any

from gns_api_gateway.api import get_user_token
from gns_api_gateway.domain import UserRole
from gns_api_gateway.infrastructure import GNS3Proxy, UserRepository

__all__ = ["GNS3Service"]


class GNS3Service:
    def __init__(self, gns3_proxy: GNS3Proxy, user_repository: UserRepository) -> None:
        self._gns3_proxy = gns3_proxy
        self._user_repository = user_repository

    async def add_project_to_user(self, project_id: str) -> None:
        user = await self._user_repository.get_user_by_token(get_user_token())
        user.add_project(project_id)
        await self._user_repository.update(user)

    async def get_user_projects(self, projects: list[dict[str, Any]]) -> list[dict[str, Any]]:
        user = await self._user_repository.get_user_by_token(get_user_token())

        if user.role == UserRole.STUDENT:
            return [p for p in projects if p["project_id"] in user.projects]

        return projects

    async def remove_project_from_user(self, project_id: str) -> None:
        user = await self._user_repository.get_user_by_token(get_user_token())
        user.delete_project(project_id)
        await self._user_repository.update(user)
