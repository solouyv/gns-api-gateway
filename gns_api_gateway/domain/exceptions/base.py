__all__ = ["BaseApiGatewayException", "NotFoundError"]


class BaseApiGatewayException(Exception):
    code = "api_gateway_exception"


class NotFoundError(BaseApiGatewayException):
    code = "not_found_error"
