import json
from contextvars import ContextVar
from typing import Optional

from .client_utils import CommonDictType
from .interfaces import IBaseAuthProvider

__all__ = ["BaseAuthProvider", "TokenAuthProvider"]


class BaseAuthProvider(IBaseAuthProvider):
    def make_headers(self) -> CommonDictType:
        return {}


class TokenAuthProvider(BaseAuthProvider):
    TOKEN_HEADER = "token"

    def __init__(self, user_context: ContextVar) -> None:
        self._user_context = user_context

    def make_headers(self) -> CommonDictType:
        headers = {}
        if user_context := self._get_user_context():
            headers[self.TOKEN_HEADER] = json.dumps(user_context)
        return headers

    def _get_user_context(self) -> Optional[CommonDictType]:
        return (
            self._user_context.get()
            if self._user_context and self._user_context.get(None)
            else None
        )
