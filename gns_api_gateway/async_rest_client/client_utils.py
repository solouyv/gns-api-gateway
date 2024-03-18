from functools import wraps
from typing import Any

from .constants import Methods
from .exceptions import AsyncRestClientError

__all__ = ["CommonDictType", "check_arguments"]

CommonDictType = dict[str, Any]


def check_arguments(func):
    @wraps(func)
    async def checking(self, *args, **kwargs):  # noqa: WPS430
        _check_methods_argument_type(kwargs)
        return await func(self, *args, **kwargs)

    return checking


def _check_methods_argument_type(kwargs: CommonDictType) -> None:
    if method := kwargs.get("method"):
        if not isinstance(method, Methods):
            raise AsyncRestClientError(
                f"Argument 'method' mast be {Methods} type, {type(method)} gotten"
            )
