from api.base import db
from api.models import PlaythroughStatuses
from api.helpers import NoChangeError
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
            'description': f"Playthrough Status item matching id {playthroughstatus_id} not found",
            'active': False
        }

    return payload


#* Mutations
@convert_kwargs_to_snake_case
def resolve_insert_playthroughstatus(obj, info, description, active):
    print("In insert resolver")
    try:
        playthroughstatus = PlaythroughStatuses(description=description, active=active)
        db.session.add(playthroughstatus)
        db.session.commit()
        
        payload = {
            'success': True,
            'field': 'PlaythroughStatus',
            'id': playthroughstatus.id
        }
    except Exception as er:
        payload = {
            'success': False,
            'errors': [er]
        }
        
    return payload

@convert_kwargs_to_snake_case
def resolve_update_playthroughstatus(obj, info, playthroughstatus_id, description=None, active=None):
    try:
        playthroughstatus = PlaythroughStatuses.query.get(playthroughstatus_id)
        recordChanged = False

        if playthroughstatus is None:
            raise AttributeError        
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
        else:
            raise NoChangeError
    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Playthrough Status item matching id {playthroughstatus_id} not found']
        }
    except NoChangeError:
        payload = {
                'success': False,
                'errors': [f'No values to change']
            }

    return payload

@convert_kwargs_to_snake_case
def resolve_delete_playthroughstatus(obj, info, playthroughstatus_id):
    try:
        playthroughstatus = PlaythroughStatuses.query.get(playthroughstatus_id)
        # TODO Find better error when record does not exist
        if playthroughstatus is None:
            raise AttributeError
        db.session.delete(playthroughstatus)
        db.session.commit()
    
        payload = {
            'success': True,
            'field': 'PlaythroughStatuses'
        }
    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Playthrough Status item matching id {playthroughstatus_id} not found'],
            'field': 'PlaythroughStatuses'
        }

    return payload
