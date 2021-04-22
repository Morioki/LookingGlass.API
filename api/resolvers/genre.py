from ariadne import convert_kwargs_to_snake_case
from api.base import db
from api.models import Genres
from api.helpers import NoChangeError


# * Genre Resolvers
def resolve_genres(_obj, _info):
    try:
        genres = [genre.to_dict() for genre in Genres.query.all()]
        print(genres)
        payload = genres
    except Exception:
        payload = None
    return payload

@convert_kwargs_to_snake_case
def resolve_genre(_obj, _info, genre_id):
    try:
        genre = Genres.query.get(genre_id)
        print(genre.to_dict())
        payload = genre.to_dict()
    except Exception:
        payload = None
    return payload


# * Mutations
@convert_kwargs_to_snake_case
def resolve_insert_genres(_obj, _info, description, parent_id=None, active=True): # pylint: disable=C0301
    try:
        genre = Genres(description=description, parentid=parent_id, active=active) # pylint: disable=C0301
        db.session.add(genre)
        db.session.commit()

        payload = {
            'success': True,
            'field': 'Genres',
            'id': genre.id
        }
    except Exception as error:
        payload = {
            'success': False,
            'errors': [error]
        }

    return payload

@convert_kwargs_to_snake_case
def resolve_update_genres(_obj, _info, genre_id, description=None,
        parent_id=None, active=None):
    try:
        genre = Genres.query.get(genre_id)
        record_changed = False
        if description is not None and genre.description != description:
            genre.description = description
            record_changed = True
        if parent_id is not None and genre.parentid != int(parent_id):
            genre.parentid = int(parent_id)
            record_changed = True
        if active is not None and genre.active != bool(active):
            genre.active = bool(active)
            record_changed = True

        if record_changed:
            db.session.commit()

            payload = {
                'success': True,
                'field': 'Genres',
                'id': genre.id
            }
        else:
            raise NoChangeError
    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Genre item matching id {genre_id} not found']
        }
    except NoChangeError:
        payload = {
            'success': False,
            'errors': ['No values to change']
        }

    return payload

@convert_kwargs_to_snake_case
def resolve_delete_genre(_obj, _info, genre_id):
    try:
        genre = Genres.query.get(genre_id)
        # TODO Find better error when record does not exist
        if genre is None:
            raise AttributeError
        db.session.delete(genre)
        db.session.commit()

        payload = {
            'success': True,
            'field': 'Genres'
        }
    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Genres item matching id {genre_id} not found'],
            'field': 'Genres'
        }

    return payload
