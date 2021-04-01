from api.base import db
from api.models import PlaythroughStatuses
from ariadne import convert_kwargs_to_snake_case


# * Queries
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


#* Mutations
# @convert_kwargs_to_snake_case
# def resolve_set_active(obj, info, playthroughstatus_id, active):
#     print("In mutation resolver!")
#     try:
#         playthroughstatus = PlaythroughStatuses.query.get(playthroughstatus_id)
#         playthroughstatus.active = bool(active)
#         db.session.commit()

#         payload = {
#             'success': True,
#             'field': 'PlaythroughStatus',
#             'id': playthroughstatus.id
#         }
#     except AttributeError:
#         payload = {
#             'success': False,
#             'errors': [f'Playthrough Stauts item matching id {playthroughstatus_id} not found']
#         }

#     return payload

@convert_kwargs_to_snake_case
def resolve_update_playthroughstatus(obj, info, playthroughstatus_id, description=None, active=None):
    print("In mutation resolver!")
    try:
        playthroughstatus = PlaythroughStatuses.query.get(playthroughstatus_id)
        recordChanged = False
        if description is not None and playthroughstatus.description != description:
            playthroughstatus.description = description
            recordChanged = True
        if active is not None and playthroughstatus.active != bool(active):
            playthroughstatus.active = bool(active)
            recordChanged = True
        
        if recordChanged:
            db.session.commit()

            payload = {
                'success': True,
                'field': 'PlaythroughStatus',
                'id': playthroughstatus.id
            }
        else: # TODO Convert to new excption type?
            payload = {
                'success': False,
                'errors': [f'No values to change']
            }
    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Playthrough Stauts item matching id {playthroughstatus_id} not found']
        }

    return payload