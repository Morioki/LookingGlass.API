
from ariadne import convert_kwargs_to_snake_case
from api.base import db
from api.models import Platforms
from api.helpers import NoChangeError

# * Platform Resolvers
@convert_kwargs_to_snake_case
def resolve_platforms(_obj, _info, generation_id=None):
    try:
        platform_query = Platforms.query
        if generation_id is not None:
            platform_query = platform_query.filter_by(generationid = generation_id) # pylint: disable=C0301
        platforms = [plat.to_dict() for plat in platform_query.all()]
        payload = platforms
    except Exception:
        payload = None
    return payload

@convert_kwargs_to_snake_case
def resolve_platform(_obj, _info, platform_id):
    try:
        platform = Platforms.query.get(platform_id)
        print(platform.to_dict())
        payload = platform.to_dict()
    except AttributeError:
        payload = None
    return payload


# * Mutations
@convert_kwargs_to_snake_case
def resolve_insert_platform(_obj, _info, generation_id, platformcode,
        description, handheld, active):
    try:
        platform = Platforms(generationid = generation_id,
            platformcode = platformcode, description = description,
            handheld = handheld, active = active)
        db.session.add(platform)
        db.session.commit()

        payload = {
            'success': True,
            'field': 'Platforms',
            'id': platform.id
        }
    except Exception as error:
        payload = {
            'success': False,
            'errors': [error]
        }

    return payload

@convert_kwargs_to_snake_case
def resolve_update_platform(_obj, _info, platform_id, generation_id=None,
        platformcode=None, description=None, handheld=None, active=None):
    try:
        platform = Platforms.query.get(platform_id)
        record_changed = False
        if generation_id is not None and platform.generationid != int(generation_id): # pylint: disable=C0301
            platform.generationid = int(generation_id)
            record_changed = True
        if platformcode is not None and platform.platformcode != platformcode:
            platform.platformcode = platformcode
            record_changed = True
        if description is not None and platform.description != description:
            platform.description = description
            record_changed = True
        if handheld is not None and platform.handheld != bool(handheld):
            platform.handheld = bool(handheld)
            record_changed = True
        if active is not None and platform.active != bool(active):
            platform.active = bool(active)
            record_changed = True

        if record_changed:
            db.session.commit()

            payload = {
                'success': True,
                'field': 'Platforms',
                'id': platform.id
            }
        else:
            raise NoChangeError
    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Platform item matching id {platform_id} not found']
        }
    except NoChangeError:
        payload = {
            'success': False,
            'errors': ['No values to change']
        }

    return payload

@convert_kwargs_to_snake_case
def resolve_delete_platform(_obj, _info, platform_id):
    try:
        platform = Platforms.query.get(platform_id)
        # TODO Find better error when record does not exist
        if platform is None:
            raise AttributeError
        db.session.delete(platform)
        db.session.commit()

        payload = {
            'success': True,
            'field': 'Platforms'
        }
    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Platforms item matching id {platform_id} not found'],
            'field': 'Platforms'
        }

    return payload
