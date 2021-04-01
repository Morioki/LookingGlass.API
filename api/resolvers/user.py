from api.models import Users
from ariadne import convert_kwargs_to_snake_case

def resolve_users(obj, info):
    # print( info.context.get('user'))
    try:
        users = [user.to_dict() for user in Users.query.all()]
        print(users)
        payload = users
    except Exception as error:
        print(error)
        payload = []
    return payload

def resolve_user(obj, info):
    try:
        user = info.context.get('user')
        print(user.to_dict())
        payload = user.to_dict()
    except AttributeError: # TODO handle error data
        pass
    return payload