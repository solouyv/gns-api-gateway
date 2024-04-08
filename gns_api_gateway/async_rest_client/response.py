import json
from dataclasses import dataclass
from typing import Any

__all__ = ["Response"]


@dataclass
class Response:
    content: bytes
    status_code: int
    headers: dict[str, Any]

    def get_content(self) -> Any:
        return json.loads(self.content)

    def change_content(self, content: Any) -> None:
        self.content = json.dumps(content).encode()
        self.headers["Content-Length"] = str(len(self.content))

    def status_code_ok(self) -> bool:
        return self.status_code < 400
