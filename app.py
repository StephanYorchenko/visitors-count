from flask import Flask

from routes import Routes

app = Flask(__name__)
app.register_blueprint(Routes)


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = (
        "no-cache, no-store, " "must-revalidate, public, " "max-age=0"
    )
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
