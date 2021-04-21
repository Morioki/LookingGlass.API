from ariadne import convert_kwargs_to_snake_case
from api.base import db
from api.models import Games, Genres, Platforms
from api.helpers import NoChangeError

# * Query
@convert_kwargs_to_snake_case
def resolve_games(__obj, info, platform_id=None, genre_id=None):
    try:
        user = info.context.get('user')
        games_query = Games.query.filter_by(userid = user.id)
        if platform_id is not None:
            games_query = games_query.filter(Games.platforms.any(id = platform_id)) # pylint: disable=C0301
        if genre_id is not None:
            games_query = games_query.filter(Games.genres.any(id = genre_id))
        games = [game.to_dict() for game in games_query.all()]
        payload = games
    except Exception as error:
        print(error)
        payload = None
    return payload

@convert_kwargs_to_snake_case
def resolve_game(_obj, info, game_id):
    try:
        user = info.context.get('user')
        game = Games.query.filter_by(userid = user.id, id = game_id).one()
        print(game.to_dict())
        payload = game.to_dict()
    except AttributeError: # TODO handle error data
        payload = None
    except Exception:
        payload = None
    return payload

# * Mutations
@convert_kwargs_to_snake_case
def resolve_insert_game(_obj, info, name, release_year, developer=None,
        publisher=None, mainseries=None, subseries=None, notes=None):
    try:
        user = info.context.get('user')
        game = Games(userid=user.id, gamename=name, releaseyear=release_year,
            developer=developer, publisher=publisher, mainseries=mainseries,
            subseries=subseries, notes=notes)

        db.session.add(game)
        db.session.commit()

        payload = {
            'success': True,
            'field': 'Games',
            'id': game.id
        }
    except Exception as error:
        payload = {
            'success': False,
            'errors': [error]
        }

    return payload

# * Note: Name / Release year cannot change
@convert_kwargs_to_snake_case
def resolve_update_game(_obj, _info, game_id, developer=None, publisher=None,
        mainseries=None, subseries=None, notes=None):
    try:
        game = Games.query.get(game_id)
        record_changed = False

        if game is None:
            raise AttributeError
        if developer is not None and game.developer != developer:
            game.developer = developer
            record_changed = True
        if publisher is not None and game.publisher != publisher:
            game.publisher = publisher
            record_changed = True
        if mainseries is not None and game.mainseries != mainseries:
            game.mainseries = mainseries
            record_changed = True
        if subseries is not None and game.subseries != subseries:
            game.subseries = subseries
            record_changed = True
        if notes is not None and game.notes != notes:
            game.notes = notes
            record_changed = True

        if record_changed:
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
            'errors': ['No values to change'],
            'field': 'Games'
        }

    return payload

@convert_kwargs_to_snake_case
def resolve_delete_game(_obj, _info, game_id):
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

@convert_kwargs_to_snake_case
def resolve_append_genre_game(_obj, _info, game_id, genre_id):
    try:
        game = Games.query.get(game_id)
        genre = Genres.query.get(genre_id)

        if game is None or genre is None:
            raise AttributeError

        game.genres.append(genre)

        db.session.commit()

        payload = {
            'success': True,
            'field': 'Games',
            'id': game.id
        }
    except AttributeError:
        payload = {
            'success': False,
            'errors': ['Invalid parameters, please review and try again'],
            'field': 'Games'
        }

    return payload

@convert_kwargs_to_snake_case
def resolve_remove_genre_game(_obj, _info, game_id, genre_id):
    try:
        game = Games.query.get(game_id)
        genre = Genres.query.get(genre_id)

        if game is None or genre is None:
            raise AttributeError

        game.genres.remove(genre)

        db.session.commit()

        payload = {
            'success': True,
            'field': 'Games',
            'id': game.id
        }

    except AttributeError:
        payload = {
            'success': False,
            'errors': ['Invalid parameters, please review and try again'],
            'field': 'Games'
        }

    return payload

@convert_kwargs_to_snake_case
def resolve_append_platform_game(_obj, _info, game_id, platform_id):
    try:
        game = Games.query.get(game_id)
        platform = Platforms.query.get(platform_id)

        if game is None or platform is None:
            raise AttributeError

        game.platforms.append(platform)

        db.session.commit()

        payload = {
            'success': True,
            'field': 'Games',
            'id': game.id
        }
    except AttributeError:
        payload = {
            'success': False,
            'errors': ['Invalid parameters, please review and try again'],
            'field': 'Games'
        }

    return payload

@convert_kwargs_to_snake_case
def resolve_remove_platform_game(_obj, _info, game_id, platform_id):
    try:
        game = Games.query.get(game_id)
        platform = Platforms.query.get(platform_id)

        if game is None or platform is None:
            raise AttributeError

        game.platforms.remove(platform)

        db.session.commit()

        payload = {
            'success': True,
            'field': 'Games',
            'id': game.id
        }
    except AttributeError:
        payload = {
            'success': False,
            'errors': ['Invalid parameters, please review and try again'],
            'field': 'Games'
        }

    return payload
