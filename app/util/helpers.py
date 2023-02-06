
from flask_restx import abort
from app.util.const import Const
from app.util.exception import DuplicateDataException,NotFoundDataException,NotPermissionException, UnauthorizedException, UnprocessableException
from werkzeug.http import HTTP_STATUS_CODES
from pydantic import ValidationError
from flask import make_response
import json, bleach

def _throw(exception):
    exceptionType = type(exception)
    if exceptionType == DuplicateDataException:
        _duplicate_abort(exception.message)
    elif exceptionType == NotFoundDataException:
        _not_found_abort(exception.message)
    elif exceptionType == NotPermissionException:
        _not_permission_abort(exception.message)
    elif exceptionType == UnauthorizedException:
        _un_authorized_abort(exception.message)
    elif exceptionType == UnprocessableException:
        _un_processable_abort(exception.message)
    else:
        _error_abort(str(exception))


def _error_abort(mess):
    """Abstraction over restplus `abort`.
    Returns error with the status code and message.
    """
    error = {
        'statusCode': 500,
        'message': mess
    }
    abort(500, **error)

def _success(message, data):
    """Abstraction over restplus `abort`.
    Returns success with the status code and message.
    """
    json_string = json.dumps(
        data, indent=4, sort_keys=True, ensure_ascii=False, default=str)
    json_string_clean = bleach.clean(json_string)
    response = {
        'statusCode': 200,
        # 'message': f"{HTTP_STATUS_CODES[200]} : {_response_message(message[0][3])}",
        'data': json.loads(json_string_clean)
    }
    return response, Const.ResponseCode.SUCCESS


def _response_message(func_name):
    func_name = func_name.replace(
        Const.SpecialChar.UNDERSCORE, Const.SpecialChar.SPACE)
    return Const.ResponseMessage.SUCCESS + func_name

def _not_permission_abort(mess):
    """Abstraction over restplus `abort`.
    Returns error with the status code and message.
    """
    error = {
        'statusCode': 413,
        'message': f"{HTTP_STATUS_CODES[412]}: {mess}",
    }
    abort(413, **error)


def _un_authorized_abort(mess):
    """Abstraction over restplus `abort`.
    Returns error with the status code and message.
    """
    error = {
        'statusCode': 401,
        'message': f"{HTTP_STATUS_CODES[401]}: {mess}",
    }
    abort(401, **error)


def _not_found_abort(mess):
    """Abstraction over restplus `abort`.
    Returns error with the status code and message.
    """
    error = {
        'statusCode': 412,
        'message': f"{HTTP_STATUS_CODES[412]}: {mess}",
    }
    abort(412, **error)

def _duplicate_abort(mess):
    error = {
        'statusCode': 409,
        'message': f"{HTTP_STATUS_CODES[409]}: {mess}",
    }
    abort(409, **error)

def _un_processable_abort(mess):
    error = {
        'statusCode': 422,
        'message': f"{HTTP_STATUS_CODES[422]}: {mess}",
    }
    abort(422, **error)

def _validation_exception(exception: ValidationError):
    error = {
        'statusCode': 403,
        'errors': exception.errors(),
        'message': 'validation errors'
    }
    return make_response(error, 403)