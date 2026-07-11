# Backend Architecture

## Objective

Build a modular, scalable, and maintainable backend for Industrial Brain using Domain-Driven Design (DDD) principles.

The backend should separate concerns clearly so that document ingestion, AI processing, graph construction, and user-facing APIs evolve independently.

---

# Technology Stack

Framework

FastAPI

Language

Python 3.12+

Database

SQLite

Knowledge Graph

Neo4j Aura

Vector Database

ChromaDB

LLM

Gemini 2.5 Flash

PDF Processing

PyMuPDF

Validation

Pydantic

Authentication

JWT

Deployment

Docker

---

# Backend Philosophy

Every feature belongs to exactly one module.

Every module owns

- Router
- Service
- Repository
- Schemas
- Utilities

No module directly accesses another module's database.

Communication happens through services.

---

# Backend Folder Structure

backend/

├── app/
│
├── main.py
│
├── core/
│   ├── config.py
│   ├── security.py
│   ├── logger.py
│   ├── constants.py
│   └── exceptions.py
│
├── database/
│   ├── sqlite.py
│   ├── neo4j.py
│   ├── chroma.py
│   └── migrations.py
│
├── modules/
│
│   ├── auth/
│   ├── documents/
│   ├── extraction/
│   ├── graph/
│   ├── embeddings/
│   ├── copilot/
│   ├── maintenance/
│   ├── analytics/
│   └── assets/
│
├── prompts/
│
├── uploads/
│
├── shared/
│
└── tests/

---

# Module Structure

Every module follows

module/

router.py

service.py

repository.py

schema.py

models.py

utils.py

---

# Example

documents/

router.py

Defines REST endpoints.

---

service.py

Business logic.

Upload

Delete

Index

Validate

---

repository.py

Reads/Writes SQLite.

---

schema.py

Request

Response

Validation

---

utils.py

File helpers.

---

# Shared Components

shared/

Contains

Response models

Enums

Validators

Exceptions

Utilities

Common helpers

---

# Configuration

core/config.py

Responsible for

Environment Variables

API Keys

Database URLs

Upload Paths

Model Names

No secrets hardcoded.

---

# Logging

core/logger.py

Logs

Uploads

Extraction

Errors

API Requests

Gemini Calls

Neo4j Queries

---

# Exception Handling

centralized

Validation Errors

Gemini Errors

Database Errors

Authentication Errors

Upload Errors

---

# Dependency Injection

FastAPI Depends()

Used for

Authentication

Database Sessions

Configuration

Services

---

# Upload Directory

uploads/

raw/

processed/

json/

chunks/

This makes debugging easy.
