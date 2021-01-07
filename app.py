from flask import Flask, Blueprint

from routes import Routes


class AppFactory:
    @staticmethod
    def make_app(routes: 'Blueprint'):
        app = Flask(__name__)
        app.register_blueprint(routes)

        @app.after_request
        def after_request(response):
            response.headers["Cache-Control"] = (
                    "no-cache, no-store, " "must-revalidate, public, " "max-age=0"
            )
            response.headers["Expires"] = 0
            response.headers["Pragma"] = "no-cache"
            return response

        return app


if __name__ == "__main__":
    app = AppFactory.make_app(Routes)
    app.run(host="0.0.0.0", port=8080)
