
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)
    descricao = db.Column(db.String(200), nullable=True)

   
    tarefas = db.relationship("Tarefa", back_populates="categoria")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
        }




class Tarefa(db.Model):
    __tablename__ = "tarefas"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(220), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="pendente")
    prioridade = db.Column(db.String(10), nullable=False, default="media")
    data_vencimento = db.Column(db.Date, nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

   
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias.id"), nullable=True)

    
    categoria = db.relationship("Categoria", back_populates="tarefas")

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "status": self.status,
            "prioridade": self.prioridade,
            "categoria": self.categoria.nome if self.categoria else None,
            "categoria_id": self.categoria_id,
            "data_vencimento": (
                self.data_vencimento.strftime("%Y-%m-%d")
                if self.data_vencimento
                else None
            ),
            "criado_em": self.criado_em.strftime("%Y-%m-%d %H:%M:%S"),
            "atualizado_em": self.atualizado_em.strftime("%Y-%m-%d %H:%M:%S"),
        }