from ariadne import convert_kwargs_to_snake_case
from api.base import db
from api.models import PlaythroughStatuses
from api.helpers import NoChangeError


# * Queries
def resolve_playthroughstatuses(_obj, _info):
    try:
        playthroughstatuses = [pt.to_dict() for pt in PlaythroughStatuses.query.all()] # pylint: disable=C0301
        payload = playthroughstatuses
    except Exception:
        payload = None
    return payload

@convert_kwargs_to_snake_case
def resolve_playthroughstatus(_obj, _info, playthroughstatus_id):
    try:
        playthroughstatus = PlaythroughStatuses.query.get(playthroughstatus_id)
        payload = playthroughstatus.to_dict()
    except AttributeError:
        payload = None
    return payload


#* Mutations
@convert_kwargs_to_snake_case
def resolve_insert_playthroughstatus(_obj, _info, description, active):
    try:
        playthroughstatus = PlaythroughStatuses(description=description,
                                                active=active)
        db.session.add(playthroughstatus)
        db.session.commit()

        payload = {
            'success': True,
            'field': 'PlaythroughStatus',
            'id': playthroughstatus.id
        }
    except Exception as error:
        payload = {
            'success': False,
            'errors': [error]
        }

    return payload

@convert_kwargs_to_snake_case
def resolve_update_playthroughstatus(_obj, _info, playthroughstatus_id,
        description=None, active=None):
    try:
        playthroughstatus = PlaythroughStatuses.query.get(playthroughstatus_id)
        record_changed = False

        if playthroughstatus is None:
            raise AttributeError
        if description is not None and playthroughstatus.description != description: # pylint: disable=C0301
            playthroughstatus.description = description
            record_changed = True
        if active is not None and playthroughstatus.active != bool(active):
            playthroughstatus.active = bool(active)
            record_changed = True

        if record_changed:
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
            'errors': [f'Playthrough Status item matching id {playthroughstatus_id} not found'] # pylint: disable=C0301
        }
    except NoChangeError:
        payload = {
                'success': False,
                'errors': ['No values to change']
            }

    return payload

@convert_kwargs_to_snake_case
def resolve_delete_playthroughstatus(_obj, _info, playthroughstatus_id):
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
            'errors': [f'Playthrough Status item matching id {playthroughstatus_id} not found'], # pylint: disable=C0301
            'field': 'PlaythroughStatuses'
        }

    return payload
