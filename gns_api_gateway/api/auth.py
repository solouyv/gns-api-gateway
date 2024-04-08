from fastapi import Request

from gns_api_gateway.constants import TOKEN_KEY
from gns_api_gateway.domain.exceptions import AuthError
from gns_api_gateway.infrastructure import user

__all__ = ["get_token", "set_user_from_token", "get_user_token"]

PUBLIC_ENDPOINTS_POSTFIXES = (
    "/docs",
    "/openapi.json",
    "/favicon.ico",
)


def get_token(request: Request) -> str:
    if token := request.query_params.get(TOKEN_KEY):
        return token

    if token := request.cookies.get(TOKEN_KEY):
        return token

    raise AuthError("Token is not provided")


def set_user_from_token(request: Request) -> None:
    if request.url.path.endswith(PUBLIC_ENDPOINTS_POSTFIXES):
        return

    token = get_token(request)
    user.set(token)


def get_user_token() -> str:
    if token := user.get(None):
        return token

    raise AuthError("Token is not provided")
