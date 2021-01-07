from flask import Blueprint

from image_generator import ImageGenerator
from infrastucture.storage import StatStorage
from .request_handler import RequestHandler


class RoutesFactory:
	@staticmethod
	def make_routes(storage: 'StatStorage',
					image_generator: 'ImageGenerator',
					request_handler_factory: 'RequestHandler'):

		handler = request_handler_factory.make(storage=storage,
											  image_generator=image_generator)

		Routes = Blueprint("routes", __name__, template_folder="templates")
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

		Routes.add_url_rule(
				"/get_image",
				"image",
				view_func=lambda: handler.get_image(),
				methods=["GET"]
		)

		return Routes
