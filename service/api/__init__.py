from sanic import Blueprint

from .query import query
from .static import static
from .mutation import mutation
from .auth import auth

api = Blueprint.group(
    query,
    static,
    auth,
    mutation,
    url_prefix='/api'
)
