from ariadne import SchemaDirectiveVisitor
from graphql import default_field_resolver, GraphQLError
from api.models import Users


def get_user_context(request):
    context = {}
    context['request'] = request
    context['user'] = None
    if "API_TOKEN" in request.headers:
        token = request.headers["API_TOKEN"]
        try:
            user = Users.query.filter_by(accesstoken = token).one()
        except Exception as er:
            # print(er)
            return context
        if user is not None:
            context['user'] = user
    return context

    

class IsAuthorizedDirective(SchemaDirectiveVisitor):
   
    def visit_field_definition(self, field, object_type):
        original_resolver = field.resolve or default_field_resolver
        
        def resolve_is_authorized(obj, info, **kwargs):
            user = info.context.get('user')
            if user is None:
                return None
                # raise GraphQLError(message="Not authorized. Invalid API Key")
            
            role = self.args.get("role") if self.args.get("role") != None else 'General'
            userroles = [role.rolename for role in user.roles]

            if role not in userroles:
                return None
                # raise GraphQLError(message="Not authorized. Permissions Insufficent")
            
            return original_resolver(obj, info, **kwargs)
            # result = original_resolver(obj, info, **kwargs)
            # return result
        
        field.resolve = resolve_is_authorized
        return field