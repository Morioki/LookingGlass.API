from api.base import db
from api.models import Playthroughs
from api.helpers import NoChangeError
from ariadne import convert_kwargs_to_snake_case

@convert_kwargs_to_snake_case
def resolve_playthroughs(obj, info, game_id=None):
    try:
        user = info.context.get('user')
        if game_id is None:
            playthroughs = [playthrough.to_dict() for playthrough in Playthroughs.query.filter_by(userid = user.id).all()]
        else:
            # TODO Potential need for param validation / sanitization
            playthroughs = [playthrough.to_dict() for playthrough in Playthroughs.query.filter_by(userid = user.id, gameid = game_id).all()]
        payload = playthroughs
    except Exception as error:
        print(error)
        payload = []
    return payload

@convert_kwargs_to_snake_case
def resolve_playthrough(obj, info, playthrough_id):
    try:
        user = info.context.get('user')
        playthrough = Playthroughs.query.filter_by(userid = user.id, id = playthrough_id).one()
        print(playthrough.to_dict())
        payload = playthrough.to_dict()
    except AttributeError: # TODO handle error data
        pass
    return payload

# * Mutations
@convert_kwargs_to_snake_case
def resolve_insert_playthrough(obj, info, game_id, type_id, status_id, notes=None):
    try:
        user = info.context.get('user')
        playthrough = Playthroughs(userid = user.id, gameid = game_id, typeid = type_id,
                statusid = status_id, notes = notes)
        
        db.session.add(playthrough)
        db.session.commit()

        payload = {
            'success': True,
            'field': 'Playthroughs',
            'id': playthrough.id
        }
    except Exception as er:
        payload = {
            'success': False,
            'errors': [er],
            'field': 'Playthroughs'
        }

    return payload

@convert_kwargs_to_snake_case
def resolve_update_playthrough(obj, info, playthrough_id, game_id=None, type_id=None,
        status_id=None, notes=None):
    try:
        playthrough = Playthroughs.query.get(playthrough_id)
        recordChanged = False

        if playthrough is None:
            raise AttributeError
        if game_id is not None and playthrough.gameid != int(game_id):
            playthrough.gameid = int(game_id)
            recordChanged = True
        if type_id is not None and playthrough.typeid != int(type_id):
            playthrough.typeid = int(type_id)
            recordChanged = True
        if status_id is not None and playthrough.statusid != int(status_id):
            playthrough.statusid = int(status_id)
            recordChanged = True
        if notes is not None and playthrough.notes != notes:
            playthrough.notes = notes
            recordChanged = True

        if recordChanged:
            db.session.commit()

            payload = {
                'success': True,
                'field': 'Playthroughs',
                'id': playthrough.id
            }
        else:
            raise NoChangeError
        
    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Playthrough item matching id {game_id} not found'],
            'field': 'Playthroughs'
        }
    except NoChangeError:
        payload = {
            'success': False,
            'errors': [f'No values to change'],
            'field': 'Playthroughs'
        }
    
    return payload

@convert_kwargs_to_snake_case
def resolve_delete_playthrough(obj, info, playthrough_id):
    try:
        playthrough = Playthroughs.query.get(playthrough_id)
        if playthrough is None:
            raise AttributeError

        db.session.delete(playthrough)
        db.session.commit()

        payload = {
            'success': True,
            'field': 'Playthroughs'
        }
    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Playthroughs item matching id {playthrough_id} not found'],
            'field': 'Playthroughs'
        }

    return payload
