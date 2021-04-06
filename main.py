# from graphql.type import schema
from graphql.type import directives
from api.base import app , db
from api import models

from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.contrib.tracing.apollotracing import ApolloTracingExtensionSync
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify
from api.resolvers import generation, platform, genre, user, game, playthroughtype, \
    playthroughstatus, playthrough, session
# from api.mutations import pl
from api.helpers import get_user_context, IsAuthorizedDirective
    
# from api.mutations import resolve_create_todo, resolve_mark_done, resolve_delete_todo, resolve_update_due_date

query = ObjectType("Query")
mutation = ObjectType("Mutation")

query.set_field('generations', generation.resolve_generations)
query.set_field('generation', generation.resolve_generation)

query.set_field('platforms', platform.resolve_platforms)
query.set_field('platform', platform.resolve_platform)

query.set_field('genres', genre.resolve_genres)
query.set_field('genre', genre.resolve_genre)

query.set_field('users', user.resolve_users)
query.set_field('user', user.resolve_user)

query.set_field('games', game.resolve_games)
query.set_field('game', game.resolve_game)

query.set_field('playthroughtypes', playthroughtype.resolve_playthroughtypes)
query.set_field('playthroughtype', playthroughtype.resolve_playthroughtype)

query.set_field('playthroughstatuses', playthroughstatus.resolve_playthroughstatuses)
query.set_field('playthroughstatus', playthroughstatus.resolve_playthroughstatus)

query.set_field('playthroughs', playthrough.resolve_playthroughs)
query.set_field('playthrough', playthrough.resolve_playthrough)

query.set_field('sessions', session.resolve_sessions)
query.set_field('session', session.resolve_session)

mutation.set_field('insertPlaythroughStatus', playthroughstatus.resolve_insert_playthroughstatus)
mutation.set_field('updatePlaythroughStatus', playthroughstatus.resolve_update_playthroughstatus)

mutation.set_field('insertPlaythroughType', playthroughtype.resolve_insert_playthroughtype)
mutation.set_field('updatePlaythroughType', playthroughtype.resolve_update_playthroughtype)

mutation.set_field('insertGeneration', generation.resolve_insert_generation)
mutation.set_field('updateGeneration', generation.resolve_update_generation)

mutation.set_field('insertPlatform', platform.resolve_insert_platform)
mutation.set_field('updatePlatform', platform.resolve_update_platform)

mutation.set_field('insertGenre', genre.resolve_insert_genres)
mutation.set_field('updateGenre', genre.resolve_update_genres)


type_defs = load_schema_from_path("./graphql/schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers, directives= {
            'isAuthorized':IsAuthorizedDirective
        }
)


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()

    success, result = graphql_sync(
        schema,
        data,
        context_value=get_user_context(request),
        # context_value=request,
        debug=app.debug
        # extensions=[ApolloTracingExtensionSync]
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code