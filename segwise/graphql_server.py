from flask_graphql import GraphQLView
from graphql.schema import schema  # Import the schema from schema.py file
from app import create_app

app = create_app()

# Add the GraphQL route for the server
app.add_url_rule(
    '/graphql', 
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)  # graphiql=True enables the GraphiQL UI
)

if __name__ == '__main__':
    app.run(debug=True)
