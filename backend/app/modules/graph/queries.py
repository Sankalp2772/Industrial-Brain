MERGE_NODE_QUERY = """
CALL apoc.merge.node([$label], {id: $id}, $properties, $properties)
YIELD node
RETURN node
"""

MERGE_RELATIONSHIP_QUERY = """
MATCH (source {id: $source_id})
MATCH (target {id: $target_id})
CALL apoc.merge.relationship(source, $rel_type, {}, $properties, target, $properties)
YIELD rel
RETURN rel
"""

# Native Cypher queries (avoiding APOC dependency for simplicity and robustness in Aura)
MERGE_DOCUMENT = """
MERGE (n:Document {id: $id})
ON CREATE SET n += $properties
ON MATCH SET n += $properties
RETURN n
"""

MERGE_ASSET = """
MERGE (n:Asset {id: $id})
ON CREATE SET n += $properties
ON MATCH SET n += $properties
RETURN n
"""

MERGE_ENGINEER = """
MERGE (n:Engineer {id: $id})
ON CREATE SET n += $properties
ON MATCH SET n += $properties
RETURN n
"""

MERGE_INSPECTION = """
MERGE (n:Inspection {id: $id})
ON CREATE SET n += $properties
ON MATCH SET n += $properties
RETURN n
"""

MERGE_INCIDENT = """
MERGE (n:Incident {id: $id})
ON CREATE SET n += $properties
ON MATCH SET n += $properties
RETURN n
"""

MERGE_MAINTENANCE_LOG = """
MERGE (n:MaintenanceLog {id: $id})
ON CREATE SET n += $properties
ON MATCH SET n += $properties
RETURN n
"""

MERGE_SOP = """
MERGE (n:SOP {id: $id})
ON CREATE SET n += $properties
ON MATCH SET n += $properties
RETURN n
"""

MERGE_WORK_ORDER = """
MERGE (n:WorkOrder {id: $id})
ON CREATE SET n += $properties
ON MATCH SET n += $properties
RETURN n
"""

MERGE_OEM_MANUAL = """
MERGE (n:OEMManual {id: $id})
ON CREATE SET n += $properties
ON MATCH SET n += $properties
RETURN n
"""

MERGE_DEPARTMENT = """
MERGE (n:Department {id: $id})
ON CREATE SET n += $properties
ON MATCH SET n += $properties
RETURN n
"""

MERGE_RELATIONSHIP_DYNAMIC = """
MATCH (source {id: $source_id})
MATCH (target {id: $target_id})
CALL apoc.create.relationship(source, $rel_type, {}, target) YIELD rel
RETURN rel
"""
# Fallback to direct cypher queries since apoc may not be enabled
def get_merge_relationship_query(rel_type: str):
    return f"""
    MATCH (source {{id: $source_id}})
    MATCH (target {{id: $target_id}})
    MERGE (source)-[r:{rel_type}]->(target)
    RETURN r
    """

GET_GRAPH_STATS = """
MATCH (n)
WITH count(n) as total_nodes
OPTIONAL MATCH ()-[r]->()
RETURN total_nodes, count(r) as total_relationships
"""

GET_ASSET_SUBGRAPH = """
MATCH (a:Asset {id: $asset_id})-[r*1..1]-(connected)
RETURN a, r, connected
"""
