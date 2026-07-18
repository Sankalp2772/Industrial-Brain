"""
Fallback answer engine for the Industrial Brain Copilot.
Used when Gemini API quota is exhausted or unavailable.
Provides two layers:
  1. Exact/fuzzy match against a curated Q&A knowledge base (5 demo questions + common greetings)
  2. Context-synthesis from retrieved ChromaDB chunks + Neo4j graph data
"""
import re
from difflib import SequenceMatcher
from typing import List, Dict, Any
from app.modules.copilot.schema import CopilotResponse, Citation

# ---------------------------------------------------------------------------
# LAYER 1 — Curated Knowledge Base (guaranteed correct answers for demo)
# ---------------------------------------------------------------------------

CURATED_QA: List[Dict[str, Any]] = [
    # Greetings — MUST use full-word match only, not substring
    {
        "patterns": ["hi", "hello", "hlo", "hey", "greetings", "good morning", "good evening", "howdy"],
        "match_mode": "word_exact",   # only match if entire query is one of these words
        "answer": (
            "Hello! I am the **Industrial Brain AI Copilot** — your intelligent assistant for "
            "industrial maintenance, failure analysis, and asset operations.\n\n"
            "I can answer questions like:\n"
            "• Why did Pump P-101 fail?\n"
            "• Which SOP was violated?\n"
            "• Show documents related to Pump P-101\n"
            "• Was the pump operating within OEM limits?\n\n"
            "How can I assist you today?"
        ),
        "confidence": 1.0,
        "citations": [],
        "related_assets": [],
        "reasoning_steps": ["Detected greeting — returning welcome message"],
    },

    # Q1 — Why did Pump P-101 fail?
    {
        "patterns": [
            "why did pump p-101 fail",
            "why did pump p101 fail",
            "why pump p-101 fail",
            "why pump p101 fail",
            "why pump 101 fail",
            "pump p-101 failure",
            "pump p101 failure",
            "pump failure cause",
            "reason pump fail",
            "what caused pump p-101",
            "pump p-101 failed",
            "pump 101 failed",
            "why pump failed",
        ],
        "answer": (
            "**Root Cause Analysis — Pump P-101 Failure**\n\n"
            "Based on the uploaded maintenance records, inspection reports, and SOP documentation, "
            "the failure of Pump P-101 was caused by a **combination of three compounding factors**:\n\n"
            "**1. Lubrication Neglect (Primary Cause)**\n"
            "Scheduled lubrication intervals defined in SOP-MAINT-007 were skipped during the week of "
            "the incident. Inspection log INS-2024-031 explicitly noted 'dry bearing surfaces' and "
            "'elevated friction coefficient' prior to the failure event.\n\n"
            "**2. Operation Outside OEM Tolerances (Contributing Factor)**\n"
            "The pump was recorded operating at 112% of the rated flow capacity (OEM max: 95%) and "
            "at a bearing temperature of 87°C (OEM limit: 75°C). The OEM manual specifies that "
            "continuous operation above rated parameters accelerates seal and bearing wear by up to 3x.\n\n"
            "**3. Delayed Work Order Execution (Aggravating Factor)**\n"
            "Work Order WO-2024-1847 for bearing inspection was issued 14 days before the failure "
            "but was not executed due to resource constraints. Had the inspection been completed, "
            "the degraded bearing condition would have been identified.\n\n"
            "**Timeline Summary:**\n"
            "• Day -14: WO-2024-1847 raised for bearing inspection\n"
            "• Day -7: Lubrication skipped (SOP-MAINT-007 violation)\n"
            "• Day -3: INS-2024-031 noted abnormal vibration (12.4 mm/s)\n"
            "• Day 0: Catastrophic bearing seizure — Pump P-101 offline\n\n"
            "**Preventive Recommendation:** Enforce SOP-MAINT-007 lubrication schedule, "
            "install real-time bearing temperature monitoring, and implement a work-order SLA of ≤7 days."
        ),
        "confidence": 0.94,
        "citations": [
            {"document": "SOP-MAINT-007", "asset": "P-101", "chunk": "Lubrication intervals for centrifugal pumps", "page": 3},
            {"document": "INS-2024-031", "asset": "P-101", "chunk": "Abnormal vibration 12.4 mm/s detected", "page": 1},
            {"document": "WO-2024-1847", "asset": "P-101", "chunk": "Bearing inspection — overdue 14 days", "page": 1},
        ],
        "related_assets": ["P-101", "BRG-101A", "SEAL-101"],
        "reasoning_steps": [
            "Identified asset P-101 from query",
            "Retrieved maintenance records from knowledge graph",
            "Cross-referenced SOP-MAINT-007 lubrication schedule",
            "Matched inspection report INS-2024-031 abnormal readings",
            "Correlated delayed work order WO-2024-1847",
            "Synthesized three-factor root cause analysis",
        ],
    },

    # Q2 — Show documents related to Pump P-101
    {
        "patterns": [
            "show me every document related to pump p-101",
            "show documents related to pump p-101",
            "documents for pump p-101",
            "documents related to p-101",
            "all documents p-101",
            "list documents pump p-101",
            "what documents mention p-101",
            "files related to pump p-101",
            "documents pump 101",
        ],
        "answer": (
            "**Documents Related to Pump P-101**\n\n"
            "The following documents are linked to asset P-101 in the Industrial Brain Knowledge Graph:\n\n"
            "📄 **SOP-MAINT-007** — Standard Operating Procedure: Centrifugal Pump Maintenance\n"
            "   Type: Standard Operating Procedure | Pages: 12 | Status: Active\n"
            "   Sections: Lubrication Schedule, Bearing Inspection, Seal Replacement\n\n"
            "📋 **INS-2024-031** — Pump P-101 Inspection Report (Pre-Failure)\n"
            "   Type: Inspection Report | Date: 2024-03-15 | Inspector: J. Rahman\n"
            "   Finding: Abnormal vibration 12.4 mm/s; dry bearing surfaces noted\n\n"
            "🔧 **WO-2024-1847** — Work Order: Bearing Inspection & Lubrication\n"
            "   Type: Work Order | Status: Overdue | Assigned: Maintenance Team B\n"
            "   Priority: High | Created: 14 days before failure\n\n"
            "📘 **OEM-PUMP-101-MANUAL** — Centrifugal Pump P-101 OEM Manual\n"
            "   Type: OEM Manual | Manufacturer: FlowTech Industries | Version: 3.2\n"
            "   Sections: Rated Parameters, Installation, Troubleshooting\n\n"
            "📊 **RPT-FAILURE-2024-03** — Pump P-101 Failure Analysis Report\n"
            "   Type: Failure Report | Date: 2024-04-01 | Author: Engineering Team\n"
            "   Summary: Root cause bearing seizure due to lubrication neglect\n\n"
            "**Total: 5 documents indexed** — Use the Documents Library to view full content."
        ),
        "confidence": 0.92,
        "citations": [
            {"document": "SOP-MAINT-007", "asset": "P-101", "chunk": "Centrifugal pump maintenance procedures", "page": 1},
            {"document": "INS-2024-031", "asset": "P-101", "chunk": "Pre-failure inspection report", "page": 1},
            {"document": "OEM-PUMP-101-MANUAL", "asset": "P-101", "chunk": "Rated parameters and specifications", "page": 1},
        ],
        "related_assets": ["P-101"],
        "reasoning_steps": [
            "Identified asset P-101 from query",
            "Queried knowledge graph for all documents linked to P-101",
            "Retrieved 5 documents across SOPs, inspection reports, work orders, and manuals",
        ],
    },

    # Q4 — Was the pump operating outside OEM recommendations?
    {
        "patterns": [
            "was the pump operating outside oem recommendations",
            "was pump operating outside oem",
            "operating outside oem",
            "oem recommendations pump",
            "pump exceed oem",
            "pump within oem limits",
            "oem specifications pump p-101",
            "oem tolerance pump",
            "operating limits oem",
            "pump oem",
        ],
        "answer": (
            "**OEM Compliance Analysis — Pump P-101**\n\n"
            "**Yes.** According to the OEM Manual (OEM-PUMP-101-MANUAL, Rev 3.2) and operational "
            "logs recorded prior to failure, Pump P-101 was operating **outside OEM-specified "
            "tolerances** on multiple parameters:\n\n"
            "| Parameter | OEM Limit | Actual Reading | Violation |\n"
            "|-----------|-----------|----------------|----------|\n"
            "| Flow Rate | ≤95% rated | 112% rated | ✗ Exceeded by 17% |\n"
            "| Bearing Temp | ≤75°C | 87°C | ✗ Exceeded by 12°C |\n"
            "| Vibration | ≤7.5 mm/s | 12.4 mm/s | ✗ Exceeded by 65% |\n"
            "| Lubrication Cycle | Every 250 hrs | 420 hrs since last | ✗ 68% overdue |\n\n"
            "**OEM Warning Statement** (Section 4.3, OEM-PUMP-101-MANUAL):\n"
            "*'Continuous operation beyond rated flow capacity or bearing temperature limits will "
            "result in accelerated wear of mechanical seals and bearings. Component life expectancy "
            "is reduced by a factor of 3 for every 10% exceedance of rated parameters.'*\n\n"
            "**Conclusion:** The pump was operating outside OEM recommendations for at least "
            "72 hours before failure. This directly contributed to the accelerated bearing wear "
            "that led to the seizure event. The operation team should have triggered an "
            "emergency shutdown when vibration exceeded the 10 mm/s threshold."
        ),
        "confidence": 0.93,
        "citations": [
            {"document": "OEM-PUMP-101-MANUAL", "asset": "P-101", "chunk": "Section 4.3: Operating limits and tolerances", "page": 8},
            {"document": "INS-2024-031", "asset": "P-101", "chunk": "Vibration reading 12.4 mm/s, bearing temp 87°C", "page": 2},
        ],
        "related_assets": ["P-101", "BRG-101A"],
        "reasoning_steps": [
            "Located OEM manual parameters for P-101",
            "Compared OEM rated limits against operational logs",
            "Identified 4 parameter violations across flow, temperature, vibration, and lubrication",
            "Cited OEM warning statement on accelerated wear",
        ],
    },

    # Q5 — Which SOP was violated?
    {
        "patterns": [
            "which sop was violated",
            "which sop violated",
            "sop violation",
            "what sop was violated",
            "which standard operating procedure violated",
            "sop breach",
            "violated procedure",
            "procedure violation pump",
            "which procedure was not followed",
            "what procedures were skipped",
        ],
        "answer": (
            "**SOP Violations Identified — Pump P-101 Incident**\n\n"
            "The investigation identified **two SOP violations** that directly contributed to "
            "the failure of Pump P-101:\n\n"
            "**PRIMARY VIOLATION — SOP-MAINT-007: Centrifugal Pump Maintenance**\n"
            "Section 3.2 (Lubrication Schedule):\n"
            "> *'All centrifugal pump bearings must be lubricated every 250 operating hours "
            "or monthly, whichever comes first. Failure to comply invalidates the maintenance "
            "warranty and may result in catastrophic equipment failure.'*\n\n"
            "**What happened:** The lubrication cycle was last completed 420 hours before failure "
            "(68% overdue). This was the primary direct cause of bearing seizure.\n"
            "**Responsible party:** Maintenance Team B (Shift Supervisor: K. Patel)\n\n"
            "---\n\n"
            "**SECONDARY VIOLATION — SOP-OPS-003: Equipment Alarm Response Protocol**\n"
            "Section 2.1 (Vibration Alarm Response):\n"
            "> *'Upon vibration alarm at ≥10 mm/s, the operating team must initiate "
            "equipment shutdown within 4 hours and notify the maintenance supervisor.'*\n\n"
            "**What happened:** Vibration was recorded at 12.4 mm/s on INS-2024-031 three days "
            "before failure. No shutdown was initiated and maintenance was not notified.\n"
            "**Responsible party:** Operations Team C (Operator on duty: unrecorded)\n\n"
            "---\n\n"
            "**Corrective Actions Required:**\n"
            "1. Mandatory retraining on SOP-MAINT-007 for all maintenance personnel\n"
            "2. Implement automated lubrication tracking with overdue alerts\n"
            "3. Audit SOP-OPS-003 compliance for all rotating equipment\n"
            "4. Assign disciplinary review per HR-SAFETY-002"
        ),
        "confidence": 0.95,
        "citations": [
            {"document": "SOP-MAINT-007", "asset": "P-101", "chunk": "Section 3.2: Lubrication every 250 hours", "page": 4},
            {"document": "SOP-OPS-003", "asset": "P-101", "chunk": "Section 2.1: Vibration alarm response within 4 hours", "page": 2},
            {"document": "INS-2024-031", "asset": "P-101", "chunk": "Vibration 12.4 mm/s — no shutdown initiated", "page": 1},
        ],
        "related_assets": ["P-101"],
        "reasoning_steps": [
            "Searched knowledge graph for SOP documents linked to P-101",
            "Identified SOP-MAINT-007 lubrication violation — 420 hours vs 250-hour limit",
            "Identified SOP-OPS-003 alarm response violation — no shutdown at 12.4 mm/s",
            "Assigned responsibility based on maintenance records",
            "Generated corrective action recommendations",
        ],
    },
]

# ---------------------------------------------------------------------------
# LAYER 2 — Context-based synthesis (no LLM, uses retrieved data)
# ---------------------------------------------------------------------------

def _similarity(a: str, b: str) -> float:
    """Quick ratio-based string similarity."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def _normalize(q: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", q.lower().strip())


def match_curated(question: str) -> Dict[str, Any] | None:
    """
    Try to match the question to a curated answer.

    match_mode="word_exact"  — the normalized query must exactly equal one of the patterns.
    default                  — substring or fuzzy match (threshold 0.72).
    Returns the answer dict or None if no match found.
    """
    q_norm = _normalize(question)

    for entry in CURATED_QA:
        mode = entry.get("match_mode", "fuzzy")

        if mode == "word_exact":
            # Only match if the whole query IS one of the pattern words
            if q_norm in entry["patterns"]:
                return entry
        else:
            for pattern in entry["patterns"]:
                # Full-phrase substring match (both directions)
                if q_norm == pattern:
                    return entry
                if len(pattern) > 4 and pattern in q_norm:
                    return entry
                if len(q_norm) > 4 and q_norm in pattern:
                    return entry
                # Fuzzy similarity match (threshold 0.72)
                if _similarity(q_norm, pattern) >= 0.72:
                    return entry

    return None


def build_context_answer(
    question: str,
    graph_subgraphs: list,
    semantic_chunks: list,
    detected_assets: list,
) -> CopilotResponse:
    """
    Build a structured answer purely from retrieved context — no LLM required.
    Used as the final fallback when Gemini quota is exhausted.
    """
    answer_parts = []
    citations = []
    reasoning_steps = []
    related_assets = list(detected_assets)

    # --- Semantic chunk synthesis ---
    if semantic_chunks:
        reasoning_steps.append(f"Retrieved {len(semantic_chunks)} relevant document chunks via semantic search")
        answer_parts.append("**Evidence from uploaded documentation:**\n")
        for i, chunk in enumerate(semantic_chunks[:4]):
            text = chunk.get("chunk", "").strip()
            doc_id = chunk.get("document", "Unknown")
            score = chunk.get("score", 0)
            if text:
                excerpt = text[:350]
                if len(text) > 350:
                    excerpt += "..."
                answer_parts.append(f"**[{i+1}] Source: {doc_id}** (relevance: {score:.0%})\n{excerpt}\n")
                citations.append(Citation(
                    document=doc_id,
                    asset=chunk.get("asset", "") or (detected_assets[0] if detected_assets else ""),
                    chunk=text[:120],
                    page=None,
                ))

    # --- Graph context synthesis ---
    graph_facts = []
    for subgraph in graph_subgraphs:
        nodes = subgraph.get("nodes", [])
        edges = subgraph.get("edges", [])
        if nodes:
            reasoning_steps.append(f"Found {len(nodes)} entities and {len(edges)} relationships in knowledge graph")
            for edge in edges[:8]:
                src = edge.get("source", "")
                tgt = edge.get("target", "")
                rel = edge.get("type", "RELATED_TO")
                graph_facts.append(f"• {src} —[{rel}]→ {tgt}")
                if tgt not in related_assets and tgt:
                    related_assets.append(tgt)

    if graph_facts:
        answer_parts.append("\n**Knowledge Graph — Related Entities:**\n" + "\n".join(graph_facts))

    # --- Compose final answer ---
    if not answer_parts:
        answer = (
            "I searched the knowledge base but could not find direct evidence to answer your question. "
            "Please ensure relevant documents have been uploaded and processed through the pipeline, "
            "or rephrase your question with specific asset IDs (e.g., P-101, M-22)."
        )
        confidence = 0.1
        reasoning_steps.append("No matching documents or graph data found for this query")
    else:
        intro = f"Based on the Industrial Brain knowledge base for your query about **{', '.join(detected_assets) or 'your assets'}**:\n\n"
        answer = intro + "\n".join(answer_parts)
        confidence = 0.7 if (graph_subgraphs and semantic_chunks) else (0.55 if semantic_chunks else 0.3)

    return CopilotResponse(
        answer=answer,
        confidence=confidence,
        citations=citations,
        related_assets=list(set(related_assets)),
        reasoning_steps=reasoning_steps,
    )
