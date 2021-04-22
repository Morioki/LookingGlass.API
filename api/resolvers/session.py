from ariadne import convert_kwargs_to_snake_case
from api.base import db
from api.models import Sessions
from api.helpers import NoChangeError

@convert_kwargs_to_snake_case
def resolve_sessions(_obj, info, playthrough_id=None, game_id=None):
    try:
        user = info.context.get('user')
        # TODO Potential need for sanitization
        if playthrough_id is None and game_id is None:
            sessions = [session.to_dict() for session in Sessions.query.filter_by(userid = user.id).all()] # pylint: disable=C0301
        elif playthrough_id is None and game_id is not None:
            sessions = [session.to_dict() for session in Sessions.query.filter_by(userid = user.id, gameid = game_id).all()] # pylint: disable=C0301
        elif playthrough_id is not None and game_id is None:
            sessions = [session.to_dict() for session in Sessions.query.filter_by(userid = user.id, playthroughid = playthrough_id).all()] # pylint: disable=C0301
        else:
            sessions = [session.to_dict() for session in Sessions.query.filter_by(userid = user.id, playthroughid = playthrough_id, gameid = game_id).all()] # pylint: disable=C0301
        payload = sessions
    except Exception as error:
        print(error)
        payload = []
    return payload

@convert_kwargs_to_snake_case
def resolve_session(_obj, info, session_id):
    try:
        user = info.context.get('user')
        session = Sessions.query.filter_by(userid = user.id, id = session_id).one() # pylint: disable=C0301
        print(session.to_dict())
        payload = session.to_dict()
    except AttributeError: # TODO handle error data
        pass
    return payload

# * Mutations
@convert_kwargs_to_snake_case
def resolve_insert_session(_obj, info, game_id, playthrough_id, startdate,
        swhours, swminutes, swseconds, swmilliseconds, notes=None):
    try:
        user = info.context.get('user')
        session = Sessions(userid = user.id, gameid = game_id,
                playthroughid = playthrough_id, startdate = startdate,
                stopwatchhours = swhours, stopwatchminutes = swminutes,
                stopwatchseconds = swseconds,
                stopwatchmilliseconds = swmilliseconds, notes = notes)

        db.session.add(session)
        db.session.commit()

        payload = {
            'success': True,
            'field': 'Sessions',
            'id': session.id
        }
    except Exception as error:
        payload = {
            'success': False,
            'errors': [error],
            'field': 'Sessions'
        }

    return payload

# pylint: disable=R0912
@convert_kwargs_to_snake_case
def resolve_update_session(_obj, _info, session_id, game_id=None,
        playthrough_id=None, startdate=None, swhours=None, swminutes=None,
        swseconds=None, swmilliseconds=None, notes=None):
    try:
        session = Sessions.query.get(session_id)
        record_changed = False

        if session is None:
            raise AttributeError
        if game_id is not None and session.gameid != int(game_id):
            session.gameid = int(game_id)
            record_changed = True
        if playthrough_id is not None and session.playthroughid != int(playthrough_id): # pylint: disable=C0301
            session.playthroughid = int(playthrough_id)
            record_changed = True
        if startdate is not None and session.startdate != startdate:
            session.startdate = startdate
            record_changed = True
        if swhours is not None and session.stopwatchhours != int(swhours):
            session.stopwatchhours = int(swhours)
            record_changed = True
        if swminutes is not None and session.stopwatchminutes != int(swminutes): # pylint: disable=C0301
            session.stopwatchminutes = int(swminutes)
            record_changed = True
        if swseconds is not None and session.stopwatchseconds != int(swseconds): # pylint: disable=C0301
            session.stopwatchseconds = int(swseconds)
            record_changed = True
        if swmilliseconds is not None and session.stopwatchmilliseconds != int(swmilliseconds): # pylint: disable=C0301
            session.stopwatchmilliseconds = int(swmilliseconds)
            record_changed = True
        if notes is not None and session.notes != notes:
            session.notes = notes
            record_changed = True

        if record_changed:
            db.session.commit()

            payload = {
                'success': True,
                'field': 'Sessions',
                'id': session.id
            }
        else:
            raise NoChangeError

    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Sessions item matching id {game_id} not found'],
            'field': 'Sessions'
        }
    except NoChangeError:
        payload = {
            'success': False,
            'errors': ['No values to change'],
            'field': 'Sessions'
        }

    return payload

@convert_kwargs_to_snake_case
def resolve_delete_session(_obj, _info, session_id):
    try:
        session = Sessions.query.get(session_id)
        if session is None:
            raise AttributeError

        db.session.delete(session)
        db.session.commit()

        payload = {
            'success': True,
            'field': 'Sessions'
        }
    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Sessions item matching id {session_id} not found'],
            'field': 'Sessions'
        }

    return payload
