from api.models import PlaythroughTypes
from ariadne import convert_kwargs_to_snake_case

def resolve_playthroughtypes(obj, info):
    try:
        playthroughtypes = [pt.to_dict() for pt in PlaythroughTypes.query.all()]
        payload = playthroughtypes
    except Exception as error:
        print(error)
        payload = []

    return payload

@convert_kwargs_to_snake_case
def resolve_playthroughtype(obj, info, playthroughtype_id):
    try:
        playthroughtype = PlaythroughTypes.query.get(playthroughtype_id)
        payload = playthroughtype.to_dict()
    except AttributeError:
        payload = {
            'id': -1,
            'description': f"Playthrough Type item matching id {playthroughtype_id} not found",
            'active': False
        }

    return payload