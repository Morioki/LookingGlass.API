from ariadne import convert_kwargs_to_snake_case
from api.base import db
from api.models import Playthroughs
from api.helpers import NoChangeError


@convert_kwargs_to_snake_case
def resolve_playthroughs(_obj, info, game_id=None, playthroughtype_id=None,
        playthroughstatus_id=None):
    try:
        user = info.context.get('user')
        playthough_query = Playthroughs.query.filter_by(userid = user.id)
        if game_id is not None:
            playthough_query = playthough_query.filter_by(gameid = game_id)
        if playthroughtype_id is not None:
            playthough_query = playthough_query.filter_by(typeid = playthroughtype_id) # pylint: disable=C0301
        if playthroughstatus_id is not None:
            playthough_query = playthough_query.filter_by(statusid = playthroughstatus_id) # pylint: disable=C0301

        # TODO Potential need for param validation / sanitization
        playthroughs = [playthrough.to_dict() for playthrough in playthough_query.all()] # pylint: disable=C0301
        payload = playthroughs
    except Exception:
        payload = None
    return payload

@convert_kwargs_to_snake_case
def resolve_playthrough(_obj, info, playthrough_id):
    try:
        user = info.context.get('user')
        playthrough = Playthroughs.query.filter_by(userid = user.id, id = playthrough_id).one() # pylint: disable=C0301
        print(playthrough.to_dict())
        payload = playthrough.to_dict()
    except AttributeError:
        payload = None
    return payload

# * Mutations
@convert_kwargs_to_snake_case
def resolve_insert_playthrough(_obj, info, game_id, type_id, status_id,
        notes=None):
    try:
        user = info.context.get('user')
        playthrough = Playthroughs(userid = user.id, gameid = game_id,
                typeid = type_id, statusid = status_id, notes = notes)

        db.session.add(playthrough)
        db.session.commit()

        payload = {
            'success': True,
            'field': 'Playthroughs',
            'id': playthrough.id
        }
    except Exception as error:
        payload = {
            'success': False,
            'errors': [error],
            'field': 'Playthroughs'
        }

    return payload

@convert_kwargs_to_snake_case
def resolve_update_playthrough(_obj, _info, playthrough_id, game_id=None,
        type_id=None, status_id=None, notes=None):
    try:
        # TODO Verify that this is limited to the UserID
        playthrough = Playthroughs.query.get(playthrough_id)
        record_changed = False

        if playthrough is None:
            raise AttributeError
        if game_id is not None and playthrough.gameid != int(game_id):
            playthrough.gameid = int(game_id)
            record_changed = True
        if type_id is not None and playthrough.typeid != int(type_id):
            playthrough.typeid = int(type_id)
            record_changed = True
        if status_id is not None and playthrough.statusid != int(status_id):
            playthrough.statusid = int(status_id)
            record_changed = True
        if notes is not None and playthrough.notes != notes:
            playthrough.notes = notes
            record_changed = True

        if record_changed:
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
            'errors': ['No values to change'],
            'field': 'Playthroughs'
        }

    return payload

@convert_kwargs_to_snake_case
def resolve_delete_playthrough(_obj, _info, playthrough_id):
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
            'errors': [f'Playthroughs item matching id {playthrough_id} not found'], # pylint: disable=C0301
            'field': 'Playthroughs'
        }

    return payload
