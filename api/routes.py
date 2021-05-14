import json
from flask import request, jsonify
from flask_cors import CORS
from ariadne import graphql_sync
from ariadne.constants import PLAYGROUND_HTML
from api.base import app
from api.helpers import get_user_context
from api.graphql import schema

CORS(app)

@app.route('/')
def hello():
    return 'Hello!'


@app.route('/graphql', methods=['GET'])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route('/graphql', methods=['POST'])
def graphql_server():
    print(request.headers)

    # data = request.get_json() if request.is_json else json.loads(request.data)
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=get_user_context(request),
        debug=app.debug
        # extensions=[ApolloTracingExtensionSync]
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code
