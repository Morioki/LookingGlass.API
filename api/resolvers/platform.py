from api.base import db
from api.models import Platforms
from api.helpers import NoChangeError
from ariadne import convert_kwargs_to_snake_case


# * Platform Resolvers
def resolve_platforms(obj, info):
    try:
        platforms = [plat.to_dict() for plat in Platforms.query.all()]
        print(platforms)
        payload = platforms
    except Exception as error:
        print(error)
        payload = []
    return payload

@convert_kwargs_to_snake_case
def resolve_platform(obj, info, platform_id):
    try:
        platform = Platforms.query.get(platform_id)
        print(platform.to_dict())
        payload = platform.to_dict()
    except AttributeError: # TODO handle error data
        pass
    return payload


# * Mutations
@convert_kwargs_to_snake_case
def resolve_insert_platform(obj, info, generation_id, platformcode, description, handheld, active):
    pass

@convert_kwargs_to_snake_case
def resolve_update_platform(obj, info, platform_id, generation_id=None, platformcode=None, description=None, handheld=None, active=None):
    pass
