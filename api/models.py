from main import db

class Platforms(db.Model):
    __tablename__ = 'platforms'
    __table_args__ = {"schema": "lg"}

    id = db.Column(db.Integer, primary_key=True)
    generationid = db.Column(db.Integer, db.ForeignKey('lg.platformgenerations.id', onupdate='CASCADE'))
    platformcode = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    handheld = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    generation = db.relationship('PlatformGenerations', backref='platforms')

    def to_dict(self):
        return {
            'id': self.id,
            'platformcode': self.platformcode,
            'description': self.description, 
            'handheld': self.handheld,
            'active': self.active,
            'generation': self.generation.to_dict(),
            'testing': self.generation
        }


class PlatformGenerations(db.Model):
    __tablename__ = 'platformgenerations'
    __table_args__ = {"schema": "lg"}

    id = db.Column(db.Integer, primary_key=True)
    generationcode = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "generationcode": self.generationcode,
            "description": self.description
        }

class Genres(db.Model):
    __tablename__ = 'genres'
    __table_args__ = {'schema': 'lg'}

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    parentid = db.Column(db.Integer, db.ForeignKey('lg.genres.id', onupdate='CASCADE'))
    active = db.Column(db.Boolean, nullable=False)

    parent = db.relationship('Genres', remote_side=[id])

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'active': self.active,
            'testing': self.parent,
            'parent': self.parent.to_dict() if self.parent is not None else None
        }