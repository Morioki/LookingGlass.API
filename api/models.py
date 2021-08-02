from sqlalchemy.sql import func
from api.base import db

usersInRoles = db.Table('usersinroles',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('userid', db.Integer, db.ForeignKey('lg.users.id')),
    db.Column('roleid', db.Integer, db.ForeignKey('lg.userroles.id')),
    schema='lg'
)

genretags = db.Table('genretags',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('gameid', db.Integer, db.ForeignKey('lg.games.id')),
    db.Column('genreid', db.Integer, db.ForeignKey('lg.genres.id')),
    schema='lg'
)

gameplatforms = db.Table('gameplatforms',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('gameid', db.Integer, db.ForeignKey('lg.games.id')),
    db.Column('platformid', db.Integer, db.ForeignKey('lg.platforms.id')),
    schema='lg'
)

class Platforms(db.Model):
    __tablename__ = 'platforms'
    __table_args__ = {'schema': 'lg'}

    id = db.Column(db.Integer, primary_key=True)
    generationid = db.Column(db.Integer,
                             db.ForeignKey('lg.platformgenerations.id',
                                           onupdate='CASCADE'))
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
    __table_args__ = {'schema': 'lg'}

    id = db.Column(db.Integer, primary_key=True)
    generationcode = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'generationcode': self.generationcode,
            'description': self.description
        }


class PlaythroughStatuses(db.Model):
    __tablename__ = 'playthroughstatus'
    __table_args__ = {'schema': 'lg'}

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'active': self.active
        }


class PlaythroughTypes(db.Model):
    __tablename__ = 'playthroughtypes'
    __table_args__ = {'schema': 'lg'}

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'active': self.active
        }


class Genres(db.Model):
    __tablename__ = 'genres'
    __table_args__ = {'schema': 'lg'}

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    parentid = db.Column(db.Integer, db.ForeignKey('lg.genres.id',
                                                   onupdate='CASCADE'),
                                                   nullable=True)
    active = db.Column(db.Boolean, nullable=False)

    parent = db.relationship('Genres', remote_side=[id])

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'active': self.active,
            'testing': self.parent,
            'parent': self.parent.to_dict() if self.parent is not None else None # pylint: disable=C0301
        }


class Users(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'lg'}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50), nullable=True)
    lastname = db.Column(db.String(50), nullable=True)
    accesstoken = db.Column(db.String(64), nullable=False)
    entrydate = db.Column(db.DateTime(timezone=True), default=func.now())

    roles = db.relationship('UserRoles',
                            secondary=usersInRoles,
                            backref='users')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'entrydate': self.entrydate.isoformat()
        }


class UserRoles(db.Model):
    __tablename__ = 'userroles'
    __table_args__ = {'schema': 'lg'}

    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(25), nullable=False)


class Games(db.Model):
    __tablename__ = 'games'
    __table_args__ = {'schema': 'lg'}

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('lg.users.id',
                                                 onupdate='CASCADE',
                                                 ondelete='CASCADE'))
    gamename = db.Column(db.String(255), nullable=False)
    releaseyear = db.Column(db.Integer, nullable=False)
    developer = db.Column(db.String(255), nullable=True)
    publisher = db.Column(db.String(255), nullable=True)
    mainseries = db.Column(db.String(255), nullable=True)
    subseries = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.String(2000), nullable=True)
    entrydate = db.Column(db.DateTime(timezone=True), default=func.now())

    user = db.relationship('Users', backref='games')
    # playthroughs = db.relationship('Playthroughs', backref='games')
    platforms = db.relationship('Platforms',
                                secondary=gameplatforms,
                                backref='games')
    genres = db.relationship('Genres',secondary=genretags, backref='games')

    def to_dict(self):
        # print(self)
        return {
            'id': self.id,
            'name': self.gamename,
            'releaseyear': self.releaseyear,
            'platforms': [platform.to_dict() for platform in self.platforms], # pylint: disable=E1133
            'genres': [genre.to_dict() for genre in self.genres], # pylint: disable=E1133
            'developer': self.developer,
            'publisher': self.publisher,
            'mainseries': self.mainseries,
            'subseries': self.subseries,
            'notes': self.notes,
            # 'playthroughs': [playthrough.to_dict() for playthrough in self.playthroughs],
            'entrydate': self.entrydate.isoformat()
        }

class Playthroughs(db.Model):
    __tablename__ = 'playthroughs'
    __table_args__ = {'schema': 'lg'}

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('lg.users.id',
                                                 onupdate='CASCADE',
                                                 ondelete='CASCADE'))
    gameid = db.Column(db.Integer, db.ForeignKey('lg.games.id',
                                                 onupdate='CASCADE',
                                                 ondelete='CASCADE'))
    typeid = db.Column(db.Integer, db.ForeignKey('lg.playthroughtypes.id',
                                                 onupdate='CASCADE'))
    statusid = db.Column(db.Integer, db.ForeignKey('lg.playthroughstatus.id',
                                                   onupdate='CASCADE'))
    notes = db.Column(db.String(2000), nullable=True)
    entrydate = db.Column(db.DateTime(timezone=True), default=func.now())

    user = db.relationship('Users', backref='playthroughs')
    game = db.relationship('Games', backref='playthroughs')
    # game = db.relationship('Games' ),
    type = db.relationship('PlaythroughTypes', backref='playthroughs')
    status = db.relationship('PlaythroughStatuses', backref='playthroughs')

    def to_dict(self):
        return {
            'id': self.id,
            'game': self.game.to_dict(),
            'type': self.type.to_dict(),
            'status': self.status.to_dict(),
            'notes': self.notes,
            'entrydate': self.entrydate.isoformat()
        }

class Sessions(db.Model):
    __tablename__ = 'sessions'
    __table_args__ = {'schema': 'lg'}

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('lg.users.id',
                                                 onupdate='CASCADE',
                                                 ondelete='CASCADE'))
    gameid = db.Column(db.Integer, db.ForeignKey('lg.games.id',
                                                 onupdate='CASCADE',
                                                 ondelete='CASCADE'))
    playthroughid = db.Column(db.Integer, db.ForeignKey('lg.playthroughs.id',
                                                        onupdate='CASCADE',
                                                        ondelete='CASCADE'))
    startdate = db.Column(db.DateTime(timezone=True))
    stopwatchhours = db.Column(db.Integer)
    stopwatchminutes = db.Column(db.Integer)
    stopwatchseconds = db.Column(db.Integer)
    stopwatchmilliseconds = db.Column(db.Integer)
    notes = db.Column(db.String(2000), nullable=True)
    entrydate = db.Column(db.DateTime(timezone=True), default=func.now())

    user = db.relationship('Users', backref='sessions')
    game = db.relationship('Games', backref='sessions')
    playthrough = db.relationship('Playthroughs', backref='sessions')

    def to_dict(self):
        return {
            'id': self.id,
            'game': self.game.to_dict(),
            'playthrough': self.playthrough.to_dict(),
            'startdate': self.startdate.isoformat(),
            'swhours': self.stopwatchhours,
            'swminutes': self.stopwatchminutes,
            'swseconds': self.stopwatchseconds,
            'swmilliseconds': self.stopwatchmilliseconds,
            'notes': self.notes,
            'entrydate': self.entrydate.isoformat()
        }
