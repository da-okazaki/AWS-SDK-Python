import os

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

ENDPOINT = os.environ.get('ENDPOINT')
API_KEY = os.environ.get('API_KEY')

print(ENDPOINT)
print(API_KEY)


_headers = {
    "Content-Type": "application/graphql",
    "x-api-key": API_KEY,
}
_transport = RequestsHTTPTransport(
    headers=_headers,
    url=ENDPOINT,
    use_json=True,
)

client = Client(
    transport=_transport,
    fetch_schema_from_transport=True,
)

mutation = gql("""
mutation CreateVisualizationCamera($input: CreateVisualizationCameraInput!) {
    createVisualizationCamera(input: $input) {
        id
        timestamp
        filename
        person_count
    }    
}
""")


variables_insert = {
    "input": {
        "id": "100",
        "timestamp": timestamp,
        "filename": file_name,
        "person_count": person_count, 
    }
}


logger.info("## Mutation")
logger.info(client.execute(mutation, variables_insert))    
