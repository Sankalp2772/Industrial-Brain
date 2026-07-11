def format_semantic_context(chunks: list) -> str:
    """
    Formats ChromaDB chunks into a readable string for the LLM prompt.
    """
    if not chunks:
        return "No semantic documentation found."
        
    context = "### DOCUMENTATION EVIDENCE ###\n"
    for i, chunk in enumerate(chunks):
        doc = chunk.get("document", "Unknown")
        text = chunk.get("chunk", "").strip()
        context += f"[Citation {i+1} - Doc: {doc}]\n{text}\n\n"
    return context

def format_graph_context(graph_data: dict) -> str:
    """
    Formats Neo4j subgraph data into a readable string for the LLM prompt.
    """
    if not graph_data or not graph_data.get("nodes"):
        return "No graph relationships found."
        
    context = "### GRAPH KNOWLEDGE EVIDENCE ###\n"
    
    nodes = {n.get("id"): n for n in graph_data.get("nodes", [])}
    edges = graph_data.get("edges", [])
    
    for edge in edges:
        src_id = edge.get("source")
        tgt_id = edge.get("target")
        rel = edge.get("type")
        
        src_type = nodes.get(src_id, {}).get("type", "Entity") if src_id in nodes else "Entity"
        tgt_type = nodes.get(tgt_id, {}).get("type", "Entity") if tgt_id in nodes else "Entity"
        
        context += f"- ({src_type}: {src_id}) --[{rel}]--> ({tgt_type}: {tgt_id})\n"
        
    return context
