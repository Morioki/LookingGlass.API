# from .models import Todo
from .models import PlatformGeneration
from .models import Platforms
from ariadne import convert_kwargs_to_snake_case

# * Generation Resolvers
def resolve_generations(obj, info):
    try:
        generations = [gen.to_dict() for gen in PlatformGeneration.query.all()]
        payload = generations
    except Exception as error:
        print(error)
        payload = []

    return payload


@convert_kwargs_to_snake_case
def resolve_generation(obj, info, generation_id):
    try:
        generation = PlatformGeneration.query.get(generation_id)
        payload = generation.to_dict()
    except AttributeError:  # todo not found
        payload = {
            'id': -1,
            'generationcode': f'N/A',
            'description': f"Generation item matching id {generation_id} not found"            
        }

    return payload

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