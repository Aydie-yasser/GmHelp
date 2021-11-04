import os

from flask import Flask

from routes.Router import Router

app = Flask(__name__, instance_relative_config=True)

# Load the configuration from the `instance` folder
app.config.from_pyfile('config.py')

# Load the file specified by the `APP_CONFIG_FILE` environment variable if set
if "APP_CONFIG_FILE" in os.environ:
    app.config.from_envvar('APP_CONFIG_FILE')

with app.app_context():
    # Load application routes from router
    router = Router()
    router.init_app_routes()

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
