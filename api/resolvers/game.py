from api.base import db
from api.models import Games
from api.helpers import NoChangeError
from ariadne import convert_kwargs_to_snake_case

# * Query
def resolve_games(obj, info):
    try:
        user = info.context.get('user')
        games = [game.to_dict() for game in Games.query.filter_by(userid = user.id).all()]
        print(games)
        payload = games
    except Exception as error:
        print(error)
        payload = []
    return payload

@convert_kwargs_to_snake_case
def resolve_game(obj, info, game_id):
    try:
        user = info.context.get('user')
        game = Games.query.filter_by(userid = user.id, id = game_id).one()
        print(game.to_dict())
        payload = game.to_dict()
    except AttributeError: # TODO handle error data
        pass
    return payload

# * Mutations
@convert_kwargs_to_snake_case
def resolve_insert_game(obj, info, name, release_year, developer=None, publisher=None, 
        mainseries=None, subseries=None, notes=None):
    try:
        user = info.context.get('user')
        game = Games(userid=user.id, gamename = name, releaseyear = release_year, 
            developer = developer, publisher = publisher, mainseries = mainseries, 
            subseries = subseries, notes = notes)
        
        db.session.add(game)
        db.session.commit()

        payload = {
            'success': True,
            'field': 'Games',
            'id': game.id
        }
    except Exception as er:
        payload = {
            'success': False,
            'errors': [er]
        }

    return payload

# * Note: Name / Release year cannot change
@convert_kwargs_to_snake_case
def resolve_update_game(obj, info, game_id, developer=None, publisher=None, 
        mainseries=None, subseries=None, notes=None):
    try:
        game = Games.query.get(game_id)
        recordChanged = False

        if game is None:
            raise AttributeError
        if developer is not None and game.developer != developer:
            game.developer = developer
            recordChanged = True
        if publisher is not None and game.publisher != publisher:
            game.publisher = publisher
            recordChanged = True
        if mainseries is not None and game.mainseries != mainseries:
            game.mainseries = mainseries
            recordChanged = True
        if subseries is not None and game.subseries != subseries:
            game.subseries = subseries
            recordChanged = True
        if notes is not None and game.notes != notes:
            game.notes = notes
            recordChanged = True

        if recordChanged:
            db.session.commit()

            payload = {
                'success': True,
                'field': 'Games',
                'id': game.id
            }
        else:
            raise NoChangeError
        
    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Game item matching id {game_id} not found'],
            'field': 'Games'
        }
    except NoChangeError:
        payload = {
            'success': False,
            'errors': [f'No values to change'],
            'field': 'Games'
        }
    
    return payload

@convert_kwargs_to_snake_case
def resolve_delete_game(obj, info, game_id):
    try:
        game = Games.query.get(game_id)
        if game is None:
            raise AttributeError

        db.session.delete(game)
        db.session.commit()

        payload = {
            'success': True,
            'field': 'Games'
        }
    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Games item matching id {game_id} not found'],
            'field': 'Games'
        }

    return payload
