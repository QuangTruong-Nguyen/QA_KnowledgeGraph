from dotenv import load_dotenv
import os

load_dotenv()


neo4j_uri = os.getenv('NEO4J_URI')
neo4j_username = os.getenv('NEO4J_USERNAME')
neo4j_password = os.getenv('NEO4J_PASSWORD')


os.environ["NEO4J_URI"] = neo4j_uri
os.environ["NEO4J_USERNAME"] = neo4j_username
os.environ["NEO4J_PASSWORD"] = neo4j_password


print(f"Neo4j URI: {os.environ['NEO4J_URI']}")
print(f"Neo4j Username: {os.environ['NEO4J_USERNAME']}")
print(f"Neo4j Password: {os.environ['NEO4J_PASSWORD']}")
