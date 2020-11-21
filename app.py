import random
from secrets import token_urlsafe

from flask import Flask

from routes import Routes

app = Flask(__name__)
app.config["SECRET_KEY"] = token_urlsafe(random.randint(1, 64))
app.register_blueprint(Routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
