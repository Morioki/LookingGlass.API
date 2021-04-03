from api.base import db
from api.models import PlatformGenerations
from api.helpers import NoChangeError
from ariadne import convert_kwargs_to_snake_case


# * Generation Resolvers
def resolve_generations(obj, info):
    try:
        generations = [gen.to_dict() for gen in PlatformGenerations.query.all()]
        payload = generations
    except Exception as error:
        print(error)
        payload = []

    return payload


@convert_kwargs_to_snake_case
def resolve_generation(obj, info, generation_id):
    try:
        generation = PlatformGenerations.query.get(generation_id)
        payload = generation.to_dict()
    except AttributeError:  # todo not found
        payload = {
            'id': -1,
            'generationcode': f'N/A',
            'description': f"Generation item matching id {generation_id} not found"            
        }

    return payload

# * Mutations
@convert_kwargs_to_snake_case
def resolve_insert_generation(obj, info, generationcode, description):
    try:
        generation = PlatformGenerations(generationcode=generationcode, description=description)
        db.session.add(generation)
        db.session.commit()

        payload = {
            'success': True,
            'field': 'PlatformGenerations',
            'id': generation.id
        }
    except Exception as er:
        payload = {
            'success': False,
            'errors': [er]
        }

    return payload

@convert_kwargs_to_snake_case
def resolve_update_generation(obj, info, generation_id, generationcode=None, description=None):
    try:
        generation = PlatformGenerations.query.get(generation_id)
        recordChanged = False
        if generationcode is not None and generation.generationcode != generationcode:
            generation.generationcode = generationcode
            recordChanged = True
        if description is not None and generation.description != description:
            generation.description = description
            recordChanged = True

        if recordChanged:
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
            'errors': [f'Platform Generation item matching id {generation_id} not found']
        }
    except NoChangeError:
        payload = {
            'success': False,
            'errors': [f'No values to change']
        }

    return payload
