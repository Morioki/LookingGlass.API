from api.models import PlaythroughStatuses
from ariadne import convert_kwargs_to_snake_case

def resolve_playthroughstatuses(obj, info):
    try:
        playthroughstatuses = [pt.to_dict() for pt in PlaythroughStatuses.query.all()]
        payload = playthroughstatuses
    except Exception as error:
        print(error)
        payload = []

    return payload

@convert_kwargs_to_snake_case
def resolve_playthroughstatus(obj, info, playthroughstatus_id):
    try:
        playthroughstatus = PlaythroughStatuses.query.get(playthroughstatus_id)
        payload = playthroughstatus.to_dict()
    except AttributeError:
        payload = {
            'id': -1,
            'description': f"Playthrough Stauts item matching id {playthroughstatus_id} not found",
            'active': False
        }

    return payload