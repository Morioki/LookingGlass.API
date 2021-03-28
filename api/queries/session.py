from api.models import Sessions
from ariadne import convert_kwargs_to_snake_case

@convert_kwargs_to_snake_case
def resolve_sessions(obj, info, playthrough_id=None, game_id=None):
    try:
        user = info.context.get('user')
        # TODO Potential need for sanitization
        if playthrough_id is None and game_id is None:
            sessions = [session.to_dict() for session in Sessions.query.filter_by(userid = user.id).all()]
        elif playthrough_id is None and game_id is not None:
            sessions = [session.to_dict() for session in Sessions.query.filter_by(userid = user.id, gameid = game_id).all()]
        elif playthrough_id is not None and game_id is None:
            sessions = [session.to_dict() for session in Sessions.query.filter_by(userid = user.id, playthroughid = playthrough_id).all()]
        else:
            sessions = [session.to_dict() for session in Sessions.query.filter_by(userid = user.id, playthroughid = playthrough_id, gameid = game_id).all()]
        # sessions = [session.to_dict() for session in Sessions.query.filter_by(userid = user.id).all()]
        # print(sessions)
        payload = sessions
    except Exception as error:
        print(error)
        payload = []
    return payload

@convert_kwargs_to_snake_case
def resolve_session(obj, info, session_id):
    try:
        user = info.context.get('user')
        session = Sessions.query.filter_by(userid = user.id, id = session_id).one()
        print(session.to_dict())
        payload = session.to_dict()
    except AttributeError: # TODO handle error data
        pass
    return payload