from api.models import Playthroughs
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