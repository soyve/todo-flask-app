from flask import jsonify, request, Blueprint
from models import db, Categoria


categorias_bp = Blueprint(
    "categorias",
    __name__,
    url_prefix="/api/categorias"
)


@categorias_bp.route("/", methods=["GET"])
def listar_categorias():
    categorias = Categoria.query.all()
    return jsonify([c.to_dict() for c in categorias]), 200



@categorias_bp.route("/", methods=["POST"])
def criar_categoria():
    dados = request.get_json()

    if not dados or not dados.get("nome"):
        return jsonify({"erro": "O campo 'nome' é obrigatório"}), 400

    if Categoria.query.filter_by(nome=dados["nome"]).first():
        return jsonify({"erro": "Já existe uma categoria com esse nome"}), 409

    nova = Categoria(
        nome=dados["nome"],
        descricao=dados.get("descricao"),
    )
    db.session.add(nova)
    db.session.commit()

    return jsonify(nova.to_dict()), 201


@categorias_bp.route("/<int:id>", methods=["DELETE"])
def deletar_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    return "", 204