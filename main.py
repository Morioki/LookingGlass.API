# from graphql.type import schema
from api.base import app , db
from api import models

from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.contrib.tracing.apollotracing import ApolloTracingExtensionSync
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify
from api.queries import generation, platform, genre
    
# from api.mutations import resolve_create_todo, resolve_mark_done, resolve_delete_todo, resolve_update_due_date

query = ObjectType("Query")
mutation = ObjectType("Mutation")

query.set_field('generations', generation.resolve_generations)
query.set_field('generation', generation.resolve_generation)

query.set_field('platforms', platform.resolve_platforms)
query.set_field('platform', platform.resolve_platform)

query.set_field('genres', genre.resolve_genres)
query.set_field('genre', genre.resolve_genre)

# mutation.set_field("createTodo", resolve_create_todo)
# mutation.set_field("markDone", resolve_mark_done)
# mutation.set_field("deleteTodo", resolve_delete_todo)
# mutation.set_field("updateDueDate", resolve_update_due_date)

# type_defs = load_schema_from_path("./graphql/sampleSchema.graphql")
# schema = make_executable_schema(
#     type_defs, query, mutation, snake_case_fallback_resolvers
# )
type_defs = load_schema_from_path("./graphql/smallSchema.graphql")
schema = make_executable_schema(
    type_defs, query, snake_case_fallback_resolvers
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
        context_value=request,
        debug=app.debug,
        # extensions=[ApolloTracingExtensionSync]
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code