import logging
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette import status
from starlette.requests import Request

from gns_api_gateway.api.serializers import ErrorModel
from gns_api_gateway.domain.exceptions import BaseApiGatewayException, NotFoundError

logger = logging.getLogger(__name__)


def json_api_gateway_exception_error_handler(error: BaseApiGatewayException, status_code: int):
    return JSONResponse(
        status_code=status_code,
        content=ErrorModel(code=error.code, message=str(error)).dict(),
    )  # noqa: WPS221


def register_error_handler(app: FastAPI) -> None:
    @app.exception_handler(BaseApiGatewayException)
    def handle_api_gateway_exception(req: Request, error: BaseApiGatewayException):  # noqa: WPS430
        mapper = [
            (NotFoundError, HTTPStatus.NOT_FOUND),
            (BaseApiGatewayException, HTTPStatus.BAD_REQUEST),
        ]

        for error_type, status_code in mapper:
            if issubclass(type(error), error_type):
                return json_api_gateway_exception_error_handler(error, status_code)

    @app.exception_handler(ValidationError)
    def bad_request(req: Request, exc: ValidationError):  # noqa: WPS430
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content=ErrorModel(code="bad_request", message=str(exc)).dict(),
        )

    @app.exception_handler(Exception)
    def handle_all_errors(req: Request, error: Exception):  # noqa: WPS430
        logger.error(f"Unhandled error {error}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorModel(code="unhandled_error", message=str(error)).dict(),
        )
