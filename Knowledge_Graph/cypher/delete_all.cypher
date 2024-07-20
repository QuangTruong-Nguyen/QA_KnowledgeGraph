// Delete all nodes and relationships
MATCH (m)-[r]->(n)
MATCH (node)
DELETE r
DELETE node