from api.base import db
from api.models import Platforms
from api.helpers import NoChangeError
from ariadne import convert_kwargs_to_snake_case

# * Platform Resolvers
def resolve_platforms(obj, info):
    try:
        platforms = [plat.to_dict() for plat in Platforms.query.all()]
        print(platforms)
        payload = platforms
    except Exception as error:
        print(error)
        payload = []
    return payload

@convert_kwargs_to_snake_case
def resolve_platform(obj, info, platform_id):
    try:
        platform = Platforms.query.get(platform_id)
        print(platform.to_dict())
        payload = platform.to_dict()
    except AttributeError: # TODO handle error data
        pass
    return payload


# * Mutations
@convert_kwargs_to_snake_case
def resolve_insert_platform(obj, info, generation_id, platformcode, 
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
    except Exception as er:
        payload = {
            'success': False,
            'errors': [er]
        }
    
    return payload

@convert_kwargs_to_snake_case
def resolve_update_platform(obj, info, platform_id, generation_id=None, 
        platformcode=None, description=None, handheld=None, active=None):
    try:
        platform = Platforms.query.get(platform_id)
        recordChanged = False
        if generation_id is not None and platform.generationid != int(generation_id):
            platform.generationid = int(generation_id)
            recordChanged = True
        if platformcode is not None and platform.platformcode != platformcode:
            platform.platformcode = platformcode
            recordChanged = True
        if description is not None and platform.description != description:
            platform.description = description
            recordChanged = True
        if handheld is not None and platform.handheld != bool(handheld):
            platform.handheld = bool(handheld)
            recordChanged = True
        if active is not None and platform.active != bool(active):
            platform.active = bool(active)
            recordChanged = True
        
        if recordChanged:
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
            'errors': [f'No values to change']
        }
    
    return payload

@convert_kwargs_to_snake_case
def resolve_delete_platform(obj, info, platform_id):
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
