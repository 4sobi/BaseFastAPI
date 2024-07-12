from http import HTTPStatus


class CustomException(Exception):
    code = HTTPStatus.BAD_GATEWAY
    message = HTTPStatus.BAD_GATEWAY.description
    data = None

    def __init__(self, message=None, data=None):
        self.error_code = self.code
        if message:
            self.message = message
        else:
            self.message = self.code.description
        if data:
            self.data = data


class BadRequestException(CustomException):
    code = HTTPStatus.BAD_REQUEST


class ConflictException(CustomException):
    code = HTTPStatus.CONFLICT


class ForbiddenException(CustomException):
    code = HTTPStatus.FORBIDDEN


class UnauthorizedException(CustomException):
    code = HTTPStatus.UNAUTHORIZED


class NotFoundException(CustomException):
    code = HTTPStatus.NOT_FOUND


class InternalServerErrorException(CustomException):
    code = HTTPStatus.INTERNAL_SERVER_ERROR
