"""The entrypoint for the flask application"""

from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from db import create_tables

app = Flask(__name__)
CORS(app)

for module in ("admin", "pets", "user", "auth"):
    __import__(module)

swagger = Swagger(app)

create_tables()

@app.route('/api/test')
def test_route():
    """
    Just a test route.

    HTTP method: any
    input: none
    output: html string
    """
    return "<h1>so skibidi</h1>"


if __name__ == '__main__':
    app.run(debug=True)
