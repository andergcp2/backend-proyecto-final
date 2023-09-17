from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Pregunta(db.Model):
    __tablename__ = "pregunta"
    id = db.Column(db.Integer, primary_key=True)
    pruebaId = db.Column(db.Integer)
    description = db.Column(db.String(1024))

class Respuesta(db.Model):
    __tablename__ = "respuesta"
    preguntaId = db.Column(db.Integer, db.ForeignKey('pregunta.id'))
    description = db.Column(db.String(240))
    correct = db.Column(db.Boolean, default=False)

class PreguntaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pregunta
        # include_relationships = True
        load_instance = True

class RespuestaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Respuesta
        include_relationships = True
        load_instance = True
