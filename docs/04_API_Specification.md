# Database Design

## Objective

Design a lightweight, scalable, and modular data storage architecture for Industrial Brain.

The system uses a hybrid storage model:

- SQLite for application data
- Neo4j Aura for knowledge graph
- ChromaDB for semantic vector search

---

# Database Architecture

Application Data
        │
        ▼
     SQLite

Knowledge Relationships
        │
        ▼
    Neo4j Aura

Semantic Search
        │
        ▼
     ChromaDB

---

# SQLite Schema

## Users

| Field | Type | Description |
|--------|------|-------------|
| id | UUID | Primary Key |
| name | TEXT | User Name |
| email | TEXT | Login Email |
| password_hash | TEXT | Encrypted Password |
| role | TEXT | Admin / Engineer |
| created_at | DATETIME | Creation Timestamp |

---

## Documents

| Field | Type |
|--------|------|
| id | UUID |
| filename | TEXT |
| original_name | TEXT |
| document_type | TEXT |
| uploaded_by | UUID |
| upload_date | DATETIME |
| processing_status | TEXT |
| page_count | INTEGER |

Processing Status

- Uploaded
- Processing
- Indexed
- Failed

---

## Assets (Cached)

| Field | Type |
|--------|------|
| asset_id | TEXT |
| asset_name | TEXT |
| asset_type | TEXT |
| manufacturer | TEXT |
| installation_date | DATE |
| location | TEXT |
| intelligence_score | INTEGER |
| health_status | TEXT |

---

## Query History

| Field | Type |
|--------|------|
| id | UUID |
| user_id | UUID |
| question | TEXT |
| answer | TEXT |
| response_time_ms | INTEGER |
| timestamp | DATETIME |

---

# Neo4j Knowledge Graph

## Node Types

Asset

Document

Engineer

SOP

Inspection

Incident

MaintenanceLog

WorkOrder

OEMManual

Department

---

## Relationship Types

(:Asset)-[:CONNECTED_TO]->(:Asset)

(:Asset)-[:FOLLOWS_SOP]->(:SOP)

(:Engineer)-[:MAINTAINED]->(:Asset)

(:Document)-[:MENTIONS]->(:Asset)

(:Asset)-[:REFERENCED_IN]->(:Document)

(:Inspection)-[:FOUND]->(:Incident)

(:Incident)-[:CAUSED]->(:Asset)

(:WorkOrder)-[:FIXES]->(:Incident)

---

# Example Graph

Pump P-101

↓

Maintenance Log

↓

Inspection

↓

Incident

↓

SOP

↓

Engineer

↓

Motor M-22

---

# ChromaDB Metadata

Each chunk stores

{
    chunk_id,
    document_id,
    asset,
    document_type,
    page,
    upload_date
}

---

# Indexing Strategy

SQLite

- Primary Keys
- Email Index
- Asset Index

Neo4j

- Asset Name
- Engineer Name
- Document ID

Chroma

- Chunk Embeddings
- Metadata Filters

---

# Data Flow

Upload

↓

SQLite Metadata

↓

Gemini Extraction

↓

Neo4j Graph

↓

Embeddings

↓

ChromaDB

---

# Data Retention

Documents

Stored locally.

Graph

Updated whenever documents change.

Embeddings

Regenerated after document updates.

---

# Future Extensions

- PostgreSQL
- Redis Cache
- Multi-Plant Architecture
- Multi-Tenant Support