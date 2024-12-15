from ariadne import ObjectType, gql, make_executable_schema
from ariadne.asgi import GraphQL

# Define the GraphQL schema
type_defs = gql(
    """
    type Query {
        hello: String!
    }
    """
)

# Create an ObjectType for the Query
query_type = ObjectType("Query")

# Resolver for the "hello" field
@query_type.field("hello")
def resolve_hello(*_):
    return "Hello world!"

# Create the executable schema
schema = make_executable_schema(type_defs, query_type)

# Create the ASGI app
app = GraphQL(schema, debug=True)
