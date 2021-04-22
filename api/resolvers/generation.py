from ariadne import convert_kwargs_to_snake_case
from api.base import db
from api.models import PlatformGenerations
from api.helpers import NoChangeError


# * Generation Resolvers
def resolve_generations(_obj, _info):
    try:
        generations = [gen.to_dict() for gen in PlatformGenerations.query.all()] # pylint: disable=C0301
        payload = generations
    except Exception:
        payload = None

    return payload


@convert_kwargs_to_snake_case
def resolve_generation(_obj, _info, generation_id):
    try:
        generation = PlatformGenerations.query.get(generation_id)
        payload = generation.to_dict()
    except AttributeError:
        payload = None

    return payload

# * Mutations
@convert_kwargs_to_snake_case
def resolve_insert_generation(_obj, _info, generationcode, description):
    try:
        generation = PlatformGenerations(generationcode=generationcode,
            description=description)
        db.session.add(generation)
        db.session.commit()

        payload = {
            'success': True,
            'field': 'PlatformGenerations',
            'id': generation.id
        }
    except Exception as error:
        payload = {
            'success': False,
            'errors': [error]
        }

    return payload

@convert_kwargs_to_snake_case
def resolve_update_generation(_obj, _info, generation_id, generationcode=None,
        description=None):
    try:
        generation = PlatformGenerations.query.get(generation_id)
        record_changed = False
        if generationcode is not None and generation.generationcode != generationcode: # pylint: disable=C0301
            generation.generationcode = generationcode
            record_changed = True
        if description is not None and generation.description != description:
            generation.description = description
            record_changed = True

        if record_changed:
            db.session.commit()

            payload = {
                'success': True,
                'field': 'PlatformGenerations',
                'id': generation.id
            }
        else:
            raise NoChangeError

    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Platform Generation item matching id {generation_id} not found'] # pylint: disable=C0301
        }
    except NoChangeError:
        payload = {
            'success': False,
            'errors': ['No values to change']
        }

    return payload

@convert_kwargs_to_snake_case
def resolve_delete_generation(_obj, _info, generation_id):
    try:
        generation = PlatformGenerations.query.get(generation_id)
        # TODO Find better error when record does not exist
        if generation is None:
            raise AttributeError
        db.session.delete(generation)
        db.session.commit()

        payload = {
            'success': True,
            'field': 'PlatformGenerations'
        }
    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Platform Generations item matching id {generation_id} not found'], # pylint: disable=C0301
            'field': 'PlatformGenerations'
        }

    return payload
