from typing import Union, Optional

from fastapi.responses import JSONResponse, Response

from gns_api_gateway.constants import JSON_CONTENT_TYPE

__all__ = ["ResponseBuilder"]

AnyPossibleContent = Union[str, bytes, dict, list, None]


class ResponseBuilder:
    def __init__(self):
        self._content_type = JSON_CONTENT_TYPE
        self._response_payload = None
        self._status_code = 200
        self._headers = {}
        self._cookie = {}

    def with_content(self, payload: AnyPossibleContent):
        if payload is not None:
            self._response_payload = payload

        return self

    def with_cookie(self, key: str, value: str):
        self._cookie[key] = value

        return self

    def with_status(self, status: Optional[int] = None):
        if status is not None:
            self._status_code = status

        return self

    def with_content_type(self, content_type: Optional[str] = None):
        if content_type is not None:
            self._content_type = content_type

        return self

    def with_headers(self, headers: Optional[dict] = None):
        if headers is not None:
            self._headers.update(headers)

        return self

    def build(self) -> Response:
        if self._is_serializable() and self._content_type == JSON_CONTENT_TYPE:
            return JSONResponse(content=self._response_payload, status_code=self._status_code, headers=self._headers)

        response = Response(
            content=self._response_payload,
            status_code=self._status_code,
            media_type=self._content_type,
            headers=self._headers,
        )

        if self._cookie:
            for key, value in self._cookie.items():
                response.set_cookie(key=key, value=value)

        return response

    def _is_serializable(self):
        return isinstance(self._response_payload, (dict, list))
