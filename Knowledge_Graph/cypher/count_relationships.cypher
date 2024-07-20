// Count num relationships
MATCH (n)-[r]->(m)
RETURN COUNT(r) as countRelationships