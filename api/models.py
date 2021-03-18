import sqlalchemy
from sqlalchemy.orm import backref
from sqlalchemy.sql.expression import false
from main import db
# from sqlalchemy.dialects.postgresql import 
# from sqlalchemy import Computed


# CREATE TABLE lg.platforms (
# 	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
# 	generationid int4 NOT NULL,
# 	platformcode varchar(10) NOT NULL,
# 	description varchar(100) NOT NULL,
# 	handheld bool NOT NULL DEFAULT false,
# 	active bool NOT NULL DEFAULT false,
# 	CONSTRAINT platforms_pkey PRIMARY KEY (id),
# 	CONSTRAINT platform_generation_fk FOREIGN KEY (generationid) REFERENCES lg.platformgenerations(id) ON UPDATE CASCADE
# );


class Platforms(db.Model):
    __tablename__ = 'platforms'
    __table_args__ = {"schema": "lg"}

    id = db.Column(db.Integer, primary_key=True)
    generationid = db.Column(db.Integer, db.ForeignKey('lg.platformgenerations.id', onupdate='CASCADE'))
    platformcode = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    handheld = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    generation = db.relationship('PlatformGeneration', backref='platforms')

    def to_dict(self):
        return {
            'id': self.id,
            'platformcode': self.platformcode,
            'description': self.description, 
            'handheld': self.handheld,
            'active': self.active,
            'generation': self.generation.to_dict()
        }


class PlatformGeneration(db.Model):
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
