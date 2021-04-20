from ariadne import SchemaDirectiveVisitor
from graphql import default_field_resolver, GraphQLError
from api.models import Users
import random
import string

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

def random_string_generator(str_size):
    return ''.join(random.choice(string.ascii_letters) for x in range(str_size))

    
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


class NoChangeError(Exception):

    def __init__(self, message='Requested update would have no effect') -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message
