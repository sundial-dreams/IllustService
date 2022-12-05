from sanic import Blueprint
import os

static = Blueprint('resource')

static.static('/resource', os.path.join(os.getcwd(), './resource'), name='resource')

