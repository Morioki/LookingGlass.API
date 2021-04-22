from ariadne import convert_kwargs_to_snake_case
from api.base import db
from api.models import PlaythroughTypes
from api.helpers import NoChangeError


# * Queries
def resolve_playthroughtypes(_obj, _info):
    try:
        playthroughtypes = [pt.to_dict() for pt in PlaythroughTypes.query.all()] # pylint: disable=C0301
        payload = playthroughtypes
    except Exception:
        payload = None

    return payload

@convert_kwargs_to_snake_case
def resolve_playthroughtype(_obj, _info, playthroughtype_id):
    try:
        playthroughtype = PlaythroughTypes.query.get(playthroughtype_id)
        payload = playthroughtype.to_dict()
    except AttributeError:
        payload = None

    return payload

# * Mutations
@convert_kwargs_to_snake_case
def resolve_insert_playthroughtype(_obj, _info, description, active):
    print("In insert resolver")
    try:
        playthroughtype = PlaythroughTypes(description=description,
                                           active=active)
        db.session.add(playthroughtype)
        db.session.commit()

        payload = {
            'success': True,
            'field': 'PlaythroughTypes',
            'id': playthroughtype.id
        }
    except Exception as error:
        payload = {
            'success': False,
            'errors': [error],
            'field': 'PlaythroughTypes'
        }

    return payload

@convert_kwargs_to_snake_case
def resolve_update_playthroughtype(_obj, _info, playthroughtype_id,
        description=None, active=None):
    try:
        playthroughtype = PlaythroughTypes.query.get(playthroughtype_id)
        record_changed = False

        if playthroughtype is None:
            raise AttributeError
        if description is not None and playthroughtype.description != description: # pylint: disable=C0301
            playthroughtype.description = description
            record_changed = True
        if active is not None and playthroughtype.active != bool(active):
            playthroughtype.active = bool(active)
            record_changed = True

        if record_changed:
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
            'errors': [f'Playthrough Type item matching id {playthroughtype_id} not found'], # pylint: disable=C0301
            'field': 'PlaythroughTypes'
        }
    except NoChangeError:
        payload = {
                'success': False,
                'errors': ['No values to change'],
                'field': 'PlaythroughTypes'
            }

    return payload

@convert_kwargs_to_snake_case
def resolve_delete_playthroughtype(_obj, _info, playthroughtype_id):
    try:
        playthrough_type = PlaythroughTypes.query.get(playthroughtype_id)
        # TODO Find better error when record does not exist
        if playthrough_type is None:
            raise AttributeError
        db.session.delete(playthrough_type)
        db.session.commit()

        payload = {
            'success': True,
            'field': 'PlaythroughTypes'
        }
    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Playthrough Type item matching id {playthroughtype_id} not found'], # pylint: disable=C0301
            'field': 'PlaythroughTypes'
        }

    return payload
