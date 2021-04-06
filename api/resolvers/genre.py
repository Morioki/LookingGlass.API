from api.base import db
from api.models import Genres
from api.helpers import NoChangeError
from ariadne import convert_kwargs_to_snake_case


# * Genre Resolvers
def resolve_genres(obj, info):
    try:
        genres = [genre.to_dict() for genre in Genres.query.all()]
        print(genres)
        payload = genres
    except Exception as error:
        print(error)
        payload = []
    return payload

@convert_kwargs_to_snake_case
def resolve_genre(obj, info, genre_id):
    try:
        genre = Genres.query.get(genre_id)
        print(genre.to_dict())
        payload = genre.to_dict()
    except Exception as error:
        pass
    return payload


# * Mutations
@convert_kwargs_to_snake_case
def resolve_insert_genres(obj, info, description, parent_id=None, active=True):
    try:
        genre = Genres(description=description, parentid=parent_id, active=active)
        # print(genre)
        db.session.add(genre)
        db.session.commit()

        payload = {
            'success': True,
            'field': 'Genres',
            'id': genre.id
        }
    except Exception as er:
        payload = {
            'success': False,
            'errors': [er]
        }
    
    return payload

@convert_kwargs_to_snake_case
def resolve_update_genres(obj, info, genre_id, description=None, parent_id=None, active=None):
    try:
        genre = Genres.query.get(genre_id)
        recordChanged = False
        if description is not None and genre.description != description:
            genre.description = description
            recordChanged = True
        if parent_id is not None and genre.parentid != int(parent_id):
            genre.parentid = int(parent_id)
            recordChanged = True
        if active is not None and genre.active != bool(active):
            genre.active = bool(active)
            recordChanged = True

        if recordChanged:
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
            'errors': [f'No values to change']
        }
    
    return payload
