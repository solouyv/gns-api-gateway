import json
from dataclasses import dataclass
from typing import Any

from .role import UserRole

__all__ = ["User"]


@dataclass
class User:
    id: int
    first_name: str
    last_name: str
    projects: set[str]
    role: UserRole

    @classmethod
    def from_dict(cls, raw_user: dict[str, Any]) -> "User":
        return User(
            id=raw_user["id"],
            first_name=raw_user["first_name"],
            last_name=raw_user["last_name"],
            projects=set(json.loads(raw_user["projects"])),
            role=UserRole(raw_user["role"]),
        )

    def to_query(self) -> str:
        return (
            f"first_name={self.first_name!r}, "
            f"last_name={self.last_name!r}, "
            f"projects={json.dumps(list(self.projects))!r}, "
            f"role={self.role.value}"
        )

    def add_project(self, project_id: str) -> None:
        self.projects.add(project_id)

    def delete_project(self, project_id: str) -> None:
        self.projects.remove(project_id)
