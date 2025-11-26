from flask import Flask, jsonify
from flask_restful import Api
from .db import db
from sqlalchemy import text
from D4F_back.service.init_service import *
from D4F_back.controller.materiel_controller import *
from D4F_back.controller.commande_controller import *
from .utils import FlaskSqlAlchemyUtils

import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env (if present) from this package folder
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)


def _get_env(*names, default=None):
    for n in names:
        v = os.getenv(n)
        if v is not None and v != "":
            return v
    return default


def build_database_uri():
    host = _get_env("FLASK_db_host")
    port = _get_env("FLASK_db_port")
    name = _get_env("FLASK_db_name")
    user = _get_env("FLASK_db_user")
    password = _get_env("FLASK_db_pass")

    return f"postgresql://{user}:{password}@{host}:{port}/{name}"

appName = "D4Fapp"
app = Flask(__name__)
# utiliser l'api fournis par flask au lieu des les réimplémenter
api = Api(app)

# Core config populated from environment/.env
app.config["SECRET_KEY"] = _get_env("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = build_database_uri()
# Prefer False (less overhead) unless explicitly enabled
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config.setdefault(50)

app.config["FLASK_RUN_PORT"] = int(_get_env("FLASK_RUN_PORT"))

# Initialize DB extension (db is a SQLAlchemy instance imported from D4F_back.db)
db.init_app(app)

# Initialize helper utilities which rely on app.config
flaskSqlAlchemyUtils = FlaskSqlAlchemyUtils(app)
materiel_service = MaterielService(app)

# Register API blueprints and import models inside app context so SQLAlchemy
# # sees the model definitions when create_all() or migrations run.
# with app.app_context():
#     # import models to register them with SQLAlchemy
#     try:
#         from . import models  # noqa: F401
#     except Exception:
#         # import failure should not break app creation; will surface on use
#         pass

#     # register blueprints
#     try:
#         from .controllers.submission_controller import bp as submissions_bp
#         app.register_blueprint(submissions_bp)
#     except Exception:
#         # if the controllers folder is missing or has errors, keep app running
#         pass


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/init_db")
def init_db():      # initialisation de la db
    flaskSqlAlchemyUtils.init_db()
    return f"DB initialized, Backend D4F running on dev environement"

@app.route("/update_db")
def update_db():    # initialisation de la db
    flaskSqlAlchemyUtils.update_db_with_new_element()
    materiel_service.import_materiels_from_csv('materiel.csv')
    return f"DB updated, Backend D4F running on dev environement"

api.add_resource(
    materielAPI,
    "/materiel",
    "/materiel/<string:materiel_id>",
)
api.add_resource(AllMaterielAPI, "/all_materiel")

api.add_resource(
    commandeAPI,
    "/commande",
    "/commande/<string:commande_id>",
)
api.add_resource(AllCommandeAPI, "/all_commande")
