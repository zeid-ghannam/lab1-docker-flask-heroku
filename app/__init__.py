from flask import Flask
from app.models import db, Person
from flask_migrate import Migrate
from config import Config
from flask_swagger_ui import get_swaggerui_blueprint
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)
    from . import routes
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.yaml'
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Person API"})
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    app.register_blueprint(routes.bp)

    return app


if __name__ == "__main__":
    app = create_app()
    # with app.app_context():
    #     db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)