# UI/UX Design & User Flow

## Objective

Design a clean, modern, enterprise-grade user experience that allows industrial engineers to quickly upload documents, explore knowledge, query AI, and analyze assets.

The UI should resemble enterprise software such as Siemens, ABB, Honeywell, SAP, and Microsoft rather than consumer AI applications.

---

# Design Principles

Our UI follows five principles.

1. Minimal

Avoid visual clutter.

---

2. Enterprise

Professional appearance suitable for industrial environments.

---

3. Explainable AI

Every AI response should include evidence, citations, and confidence.

---

4. Fast Navigation

Users should reach any major feature within two clicks.

---

5. Consistent Components

All pages use the same cards, buttons, tables, typography, colors, and spacing.

---

# Design System

## Colors

Primary

Blue

Secondary

Slate Gray

Success

Green

Warning

Orange

Critical

Red

Background

Light Gray

Cards

White

---

## Typography

Headings

Bold

Modern Sans Serif

Body

Readable

Medium weight

Code

Monospace

---

## Icons

Lucide Icons

---

## Components

Buttons

Cards

Tables

Badges

Progress Bars

Timeline

Search Bar

Navigation Drawer

Dialogs

Upload Components

Charts

Status Chips

---

# Navigation Structure

Dashboard

↓

Documents

↓

Knowledge Graph

↓

Assets

↓

AI Copilot

↓

Analytics

↓

Settings

---

# Screen 1

Landing Page

Purpose

Introduce the product.

Sections

Hero

Features

Architecture Overview

Business Impact

Call To Action

Footer

---

# Screen 2

Login

Components

Email

Password

Remember Me

Login Button

Forgot Password

---

# Screen 3

Dashboard

Top Cards

Documents

Assets

Knowledge Coverage

Critical Assets

Average Response Time

Recent Uploads

Recent AI Queries

Quick Actions

Upload

Search

Copilot

Knowledge Graph

---

# Screen 4

Document Upload

Components

Drag and Drop

Upload Button

Upload Queue

Processing Status

Document Preview

Metadata

Entity Extraction Preview

---

# Screen 5

Documents Library

Features

Search

Filter

Sort

Processing Status

Document Type

Upload Date

View Details

Delete

---

# Screen 6

Knowledge Graph

Features

Interactive Graph

Search Node

Filter

Relationship Panel

Node Details

Mini Map

Click Node

↓

Open Asset Page

---

# Screen 7

Asset Dashboard

Sections

Asset Overview

Industrial Intelligence Score

Health Indicator

Timeline

Related Documents

Related Assets

Inspection Summary

Maintenance History

Incident History

AI Summary

Maintenance Intelligence

Suggested Questions

---

# Screen 8

Industrial AI Copilot

Layout

Left

Chat History

Center

Conversation

Right

Evidence

Confidence

Related Documents

Related Assets

Suggested Questions

Example Questions

Why did Pump P-101 fail?

Show maintenance history.

Which SOP applies?

Compare Pump P-101 and Motor M-22.

---

# Screen 9

Analytics

Cards

Assets

Documents

Knowledge Coverage

Queries

Charts

Asset Health

Failure Trends

Document Types

Knowledge Growth

Recent Activity

---

# Screen 10

Settings

Profile

Theme

API Status

About

Logout

---

# User Flow

Login

↓

Dashboard

↓

Upload Documents

↓

Processing

↓

Knowledge Graph Updated

↓

Search Asset

↓

Open Asset Dashboard

↓

Ask AI

↓

Receive Evidence-backed Answer

↓

Maintenance Recommendation

---

# Antigravity Development Plan

Generate pages in the following order.

1.

Design System

2.

Landing Page

3.

Login

4.

Dashboard

5.

Upload Page

6.

Documents Library

7.

Knowledge Graph

8.

Asset Dashboard

9.

AI Copilot

10.

Analytics

11.

Settings

12.

Connect all pages with React Router

13.

Create reusable components

14.

Replace mock APIs with FastAPI APIs

---

# Antigravity Prompt Strategy

Prompt 1

Design System

Prompt 2

Landing Page

Prompt 3

Dashboard

Prompt 4

Upload Center

Prompt 5

Knowledge Graph

Prompt 6

Asset Dashboard

Prompt 7

Industrial AI Copilot

Prompt 8

Analytics

Prompt 9

Settings

Prompt 10

Application Integration

---

# UI Success Criteria

Modern Enterprise UI

Fast Navigation

Reusable Components

Responsive Layout

Consistent Branding

Professional Industrial Theme