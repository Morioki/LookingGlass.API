from api.models import Genres
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
