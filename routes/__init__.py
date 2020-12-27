from flask import Blueprint

from infrastucture.storage import StatStorage
from infrastucture.sql_executor import SQLExecutor
from .request_handler import RequestHandler

Routes = Blueprint("routes", __name__, template_folder="templates")
sql = SQLExecutor()
storage = StatStorage(sql)
handler = RequestHandler(storage)

Routes.add_url_rule(
    "/update_count",
    "update",
    view_func=lambda: handler.update_count(),
    methods=["GET"]
)

Routes.add_url_rule(
    "/get_count",
    "count",
    view_func=lambda: handler.get_count(),
    methods=["GET"]
)
