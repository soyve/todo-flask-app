from flask import Flask, jsonify, send_from_directory
from models import db

from routes.categorias import categorias_bp
from routes.tarefas import tarefas_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tarefas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(categorias_bp)
app.register_blueprint(tarefas_bp)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return jsonify({"mensagem": "API de tarefas funcionando!"})


@app.route("/front")
def front():
    return send_from_directory("static", "index.html")


if __name__ == "__main__":
    app.run(debug=True)