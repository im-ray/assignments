from flask import Flask
from graphene import Schema, ObjectType, String
from flask_graphql import GraphQLView

class Query(ObjectType):
    hello = String(name=String(default_value="stranger"))

    def resolve_hello(self, info, name):
        return f"Hello, {name}"

schema = Schema(query=Query)

app = Flask(__name__)

# Add the GraphQL route
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run(debug=True)
