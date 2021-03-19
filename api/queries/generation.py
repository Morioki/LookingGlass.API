from api.models import PlatformGenerations
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
