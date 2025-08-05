from weaviate import Client


def get_weaviate_client():
    return Client("http://localhost:8080")

def setup_weaviate_schema(client):
    schema = {
        "class": "InsuranceChunk",
        "vectorizer": "none",
        "properties": [
            {"name": "text", "dataType": ["text"]},
            {"name": "section", "dataType": ["text"]}
        ]
    }
    if not client.schema.exists("InsuranceChunk"):
        client.schema.create_class(schema)