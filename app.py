from flask import Flask, Blueprint

from image_generator import ImageGenerator
from infrastucture import SQLExecutor, StatStorage
from routes import RoutesFactory, RequestHandler


class AppFactory:
    @staticmethod
    def make_app(routes: 'Blueprint'):
        app = Flask(__name__)

        app.register_blueprint(routes)

        @app.after_request
        def after_request(response):
            response.headers["Cache-Control"] = (
                    "no-cache, no-store, " "must-revalidate, public, "
                    "max-age=0"
            )
            response.headers["Expires"] = 0
            response.headers["Pragma"] = "no-cache"
            return response

        return app


if __name__ == "__main__":
    sql_executor = SQLExecutor()
    storage = StatStorage.make_with_executor(sql_executor)
    image_generator = ImageGenerator()
    routes = RoutesFactory.make_routes(storage,
                                       image_generator,
                                       RequestHandler)
    app = AppFactory.make_app(routes)
    app.run(host="0.0.0.0", port=8080)
