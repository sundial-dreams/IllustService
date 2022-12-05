from sanic.response import json, HTTPResponse


# err_no

def no_auth_error(message: str = '', err_no: int = 1) -> HTTPResponse:
    return json({
        'errno': err_no,
        'message': message
    }, status=401)

def auth_expired_error(message: str = '', err_no: int = 2) -> HTTPResponse:
    return json({
        'errno': err_no,
        'message': message
    }, status=401)
