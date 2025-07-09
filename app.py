from flask import Flask
from routes import add_namespaces
from flask_restx import Api
from db import db
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dotori.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

api = Api(app, doc="/docs")
add_namespaces(api)
if __name__ == "__main__":
    app.run(debug=True)
