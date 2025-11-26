from sqlalchemy import text
import os
from D4F_back.db import db
from D4F_back.service.init_service import *

def est_un_nouvel_objet(bool_existance, instance_objet):
    return {"is_new":bool_existance, 'instance':instance_objet}

class FlaskSqlAlchemyUtils:

    def __init__(self, app):
        self.app = app
        self.db = db
        # Use DB URI already set in app.config by the application initializer.
        # If not present, fall back to environment variables (defensive),
        # but avoid printing or leaking sensitive information.
        db_uri = app.config.get("SQLALCHEMY_DATABASE_URI")
        if not db_uri:
            host = os.getenv("FLASK_db_host") or os.getenv("FLASK_DB_HOST")
            port = os.getenv("FLASK_db_port") or os.getenv("FLASK_DB_PORT")
            name = os.getenv("FLASK_db_db") or os.getenv("FLASK_db_name") or os.getenv("FLASK_DB_NAME")
            user = os.getenv("FLASK_db_user") or os.getenv("FLASK_DB_USER")
            password = os.getenv("FLASK_db_pass") or os.getenv("FLASK_DB_PASS")
            if user and name:
                db_uri = f"postgresql://{user}:{password or ''}@{host or 'localhost'}:{port or '5432'}/{name}"
                app.config["SQLALCHEMY_DATABASE_URI"] = db_uri

        # Prefer False to avoid the overhead unless explicitly enabled
        app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)
        app.config.setdefault("SQLALCHEMY_POOL_SIZE", 50)

    def init_db(self,):
        with self.app.app_context():
            self.db.create_all()
            

    def update_db_with_new_element(self):
        with self.app.app_context():
            self.db.create_all()