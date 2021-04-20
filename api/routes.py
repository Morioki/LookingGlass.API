from api.base import app
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify
from ariadne import graphql_sync
from api.helpers import get_user_context
from api.graphql import schema

@app.route('/')
def hello():
    return 'Hello!'


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


# TODO How to handle key errors if users provide wrong key ids
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