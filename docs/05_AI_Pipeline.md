# API Design

## Objective

Provide REST APIs for frontend communication and AI orchestration.

---

# Authentication APIs

## Login

POST /auth/login

Request

{
    "email": "",
    "password": ""
}

Response

{
    "token": "",
    "user": {}
}

---

## Register

POST /auth/register

---

# Document APIs

## Upload Document

POST /documents/upload

Form Data

file

Response

{
    "document_id":"",
    "status":"uploaded"
}

---

## List Documents

GET /documents

---

## Get Document

GET /documents/{id}

---

## Delete Document

DELETE /documents/{id}

---

# Asset APIs

## List Assets

GET /assets

---

## Asset Details

GET /assets/{asset_id}

Returns

- Asset Details
- Timeline
- Related Documents
- Intelligence Score
- Maintenance Summary

---

# Graph APIs

## Complete Graph

GET /graph

---

## Asset Graph

GET /graph/{asset_id}

---

# AI Copilot

POST /copilot/query

Request

{
    "question":"Why did Pump P-101 fail?"
}

Response

{
    "answer":"...",
    "confidence":0.94,
    "sources":[
        "ML-001",
        "INS-001",
        "INC-001"
    ],
    "related_assets":[
        "Pump P-101"
    ]
}

---

# Maintenance Intelligence

GET /maintenance/{asset_id}

Returns

{
    "risk":"High",
    "recommendations":[
        "...",
        "..."
    ],
    "evidence":[
        "Maintenance Log",
        "Inspection Report"
    ]
}

---

# Analytics

GET /analytics

Returns

{
    "documents":15,
    "assets":3,
    "queries":32,
    "critical_assets":1
}

---

# Health Check

GET /health

Returns

{
    "status":"running"
}

---

# API Flow

React

↓

FastAPI

↓

Gemini

↓

Neo4j

↓

Chroma

↓

Response

---

# HTTP Status Codes

200 Success

201 Created

400 Bad Request

401 Unauthorized

404 Not Found

500 Internal Error

---

# Security

JWT Authentication

Password Hashing

Environment Variables

HTTPS Ready

---

# Future APIs

- Bulk Upload

- User Roles

- Audit Logs

- Notifications

- WebSockets