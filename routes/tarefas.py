from flask import Blueprint, jsonify, request
from models import db, Tarefa, Categoria
from datetime import datetime

tarefas_bp = Blueprint(
    "tarefas",
    __name__,
    url_prefix="/api/tarefas"
)


@tarefas_bp.route("/", methods=["GET"])
def listar_tarefas():
    query = Tarefa.query

    status = request.args.get("status")
    if status:
        query = query.filter_by(status=status)

    prioridade = request.args.get("prioridade")
    if prioridade:
        query = query.filter_by(prioridade=prioridade)

    categoria_id = request.args.get("categoria_id", type=int)
    if categoria_id:
        query = query.filter_by(categoria_id=categoria_id)

    tarefas = query.all()
    return jsonify([t.to_dict() for t in tarefas]), 200


@tarefas_bp.route("/<int:id>", methods=["GET"])
def buscar_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    return jsonify(tarefa.to_dict()), 200



@tarefas_bp.route("/", methods=["POST"])
def criar_tarefa():
    dados = request.get_json()

    if not dados or not dados.get("titulo"):
        return jsonify({"erro": "O campo 'titulo' é obrigatório"}), 400

    categoria_id = dados.get("categoria_id")
    if categoria_id and not Categoria.query.get(categoria_id):
        return jsonify({"erro": "Categoria não encontrada"}), 404

    nova_tarefa = Tarefa(
        titulo=dados["titulo"],
        descricao=dados.get("descricao"),
        status=dados.get("status", "pendente"),
        prioridade=dados.get("prioridade", "media"),
        categoria_id=categoria_id,
    )

    if dados.get("data_vencimento"):
        nova_tarefa.data_vencimento = datetime.strptime(
            dados["data_vencimento"], "%Y-%m-%d"
        ).date()

    db.session.add(nova_tarefa)
    db.session.commit()

    return jsonify(nova_tarefa.to_dict()), 201


@tarefas_bp.route("/<int:id>", methods=["PUT"])
def atualizar_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    if "titulo" in dados:
        tarefa.titulo = dados["titulo"]
    if "descricao" in dados:
        tarefa.descricao = dados["descricao"]
    if "status" in dados:
        tarefa.status = dados["status"]
    if "prioridade" in dados:
        tarefa.prioridade = dados["prioridade"]
    if "data_vencimento" in dados:
        tarefa.data_vencimento = datetime.strptime(
            dados["data_vencimento"], "%Y-%m-%d"
        ).date()

    if "categoria_id" in dados:
        categoria_id = dados["categoria_id"]
        if categoria_id and not Categoria.query.get(categoria_id):
            return jsonify({"erro": "Categoria não encontrada"}), 404
        tarefa.categoria_id = categoria_id

    tarefa.atualizado_em = datetime.utcnow()
    db.session.commit()

    return jsonify(tarefa.to_dict()), 200



@tarefas_bp.route("/<int:id>", methods=["DELETE"])
def deletar_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    db.session.delete(tarefa)
    db.session.commit()
    return "", 204