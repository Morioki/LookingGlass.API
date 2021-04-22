from ariadne import convert_kwargs_to_snake_case
from api.models import Users


def resolve_users(_obj, _info):
    try:
        users = [user.to_dict() for user in Users.query.all()]
        payload = users
    except Exception:
        payload = None
    return payload

def resolve_user(_obj, info):
    try:
        user = info.context.get('user')
        print(user.to_dict())
        payload = user.to_dict()
    except AttributeError: # TODO handle error data
        payload = None
    return payload
