from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Prueba(db.Model):
    __tablename__ = "prueba"
    id = db.Column(db.Integer, primary_key=True)
    categoryId = db.Column(db.Integer)
    name = db.Column(db.String(50))
    createdAt = db.Column(db.DateTime)

@property
def createdAt(self):
    return self.createdAt.isoformat()

class PruebaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Prueba
        # include_relationships = True
        load_instance = True
