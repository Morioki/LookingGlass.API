from api.base import db
from api.models import PlaythroughTypes
from api.helpers import NoChangeError
from ariadne import convert_kwargs_to_snake_case

# * Queries 
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

# * Mutations
@convert_kwargs_to_snake_case
def resolve_insert_playthroughtype(obj, info, description, active):
    print("In insert resolver")
    try:
        playthroughtype = PlaythroughTypes(description=description, active=active)
        db.session.add(playthroughtype)
        db.session.commit()
        
        payload = {
            'success': True,
            'field': 'PlaythroughTypes',
            'id': playthroughtype.id
        }
    except Exception as er:
        payload = {
            'success': False,
            'errors': [er],
            'field': 'PlaythroughTypes'
        }
        
    return payload

@convert_kwargs_to_snake_case
def resolve_update_playthroughtype(obj, info, playthroughtype_id, description=None, active=None):
    try:
        playthroughtype = PlaythroughTypes.query.get(playthroughtype_id)
        recordChanged = False

        if playthroughtype is None:
            raise AttributeError
        if description is not None and playthroughtype.description != description:
            playthroughtype.description = description
            recordChanged = True
        if active is not None and playthroughtype.active != bool(active):
            playthroughtype.active = bool(active)
            recordChanged = True
        
        if recordChanged:
            db.session.commit()

            payload = {
                'success': True,
                'field': 'PlaythroughTypes',
                'id': playthroughtype.id
            }
        else: 
            raise NoChangeError
    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Playthrough Type item matching id {playthroughtype_id} not found'],
            'field': 'PlaythroughTypes'
        }
    except NoChangeError:
        payload = {
                'success': False,
                'errors': [f'No values to change'],
                'field': 'PlaythroughTypes'
            }

    return payload

@convert_kwargs_to_snake_case
def resolve_delete_playthroughtype(obj, info, playthroughtype_id):
    try:
        playthroughType = PlaythroughTypes.query.get(playthroughtype_id)
        # TODO Find better error when record does not exist
        if playthroughType is None:
            raise AttributeError
        db.session.delete(playthroughType)
        db.session.commit()
    
        payload = {
            'success': True,
            'field': 'PlaythroughTypes'
        }
    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Playthrough Type item matching id {playthroughtype_id} not found'],
            'field': 'PlaythroughTypes'
        }

    return payload
