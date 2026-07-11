# System Architecture

## Objective

Design a scalable and modular architecture capable of transforming industrial documents into connected organizational knowledge.

---

## High-Level Architecture

User

↓

React Frontend

↓

FastAPI Backend

↓

Document Processing

↓

Knowledge Layer

↓

Industrial AI Copilot

---

## Technology Stack

Frontend

- React
- TypeScript
- Tailwind CSS
- Shadcn UI

Backend

- FastAPI
- Python

AI

- Gemini API

Knowledge Graph

- Neo4j Aura

Vector Database

- ChromaDB

Database

- SQLite

Deployment

- Docker

---

## Architecture Layers

### Presentation Layer

Responsibilities

- Dashboard
- Upload Interface
- AI Chat
- Graph Visualization

---

### API Layer

Responsibilities

- Authentication
- Upload APIs
- Query APIs
- Asset APIs

---

### AI Processing Layer

Responsibilities

- OCR
- Entity Extraction
- Relationship Extraction
- Embedding Generation

---

### Knowledge Layer

Components

Neo4j

Stores

- Assets
- Documents
- Engineers
- SOPs
- Relationships

ChromaDB

Stores

- Vector embeddings
- Chunk metadata

SQLite

Stores

- Users
- Documents
- Query history

---

## Document Processing Flow

Upload

↓

Document Type Detection

↓

OCR (if required)

↓

Text Extraction

↓

Gemini Structured Extraction

↓

Neo4j

+

ChromaDB

↓

Searchable Knowledge

---

## Query Flow

User Question

↓

Entity Detection

↓

Knowledge Graph Traversal

↓

Vector Search

↓

Context Assembly

↓

Gemini Response

↓

Answer with Citations

---

## Folder Structure

backend/

frontend/

docs/

sample-data/

presentation/

---

## Performance Targets

Document Processing

<15 seconds

AI Response

<5 seconds

Graph Loading

<2 seconds

Dashboard Loading

<2 seconds

---

## Deployment

Frontend

React

Backend

FastAPI Docker Container

Knowledge Graph

Neo4j Aura

Vector Database

Embedded ChromaDB

LLM

Gemini API

---

## Failure Strategy

If extraction fails

- Preserve uploaded file
- Retry processing
- Notify user

If Gemini becomes unavailable

- Continue using pre-ingested knowledge graph

---

## Scalability

Future improvements

- Multi-plant support
- Multi-language support
- Live IoT integration
- ERP integration
- Predictive Maintenance Models