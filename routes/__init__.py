from flask import Blueprint
from . import test_pages, domain

Routes = Blueprint('routes', __name__, template_folder='templates')

Routes.add_url_rule(
    '/', 'test_page', view_func=test_pages.test_page, methods=["GET"]
)

Routes.add_url_rule(
	'/test_page', 'test_page', view_func=test_pages.test_page, methods=["GET"]
)

Routes.add_url_rule(
	'/test_page1', 'testpage1', view_func=test_pages.test_page, methods=["GET"]
)

Routes.add_url_rule(
	'/update_count', 'update', view_func=domain.update_count, methods=["GET"]
)

Routes.add_url_rule(
	'/get_count', 'count', view_func=domain.get_count, methods=["GET"]
)

