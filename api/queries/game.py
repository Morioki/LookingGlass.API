from api.models import Games
from ariadne import convert_kwargs_to_snake_case

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