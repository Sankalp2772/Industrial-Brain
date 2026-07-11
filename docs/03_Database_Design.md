# Dataset & Knowledge Engineering

## Objective

Design a connected industrial knowledge ecosystem capable of demonstrating cross-document reasoning.

---

## Company

IndTech Manufacturing Pvt. Ltd.

Industry

Heavy Industrial Manufacturing

Plant

Plant A

---

## Primary Assets

Pump P-101

Motor M-22

Compressor C-07

---

## Departments

Maintenance

Operations

Safety

Quality

---

## Engineers

Rahul Sharma

Maintenance Engineer

Priya Nair

Inspection Engineer

Arjun Mehta

Plant Manager

---

## Storyline

The entire dataset revolves around one operational incident.

Pump P-101 experienced increasing vibration due to delayed maintenance.

Maintenance logs recorded skipped lubrication.

Inspection reports identified bearing wear.

The issue eventually caused an equipment failure and emergency shutdown.

The AI must connect these documents to explain the complete chain of events.

Motor M-22 serves as a positive comparison where timely maintenance prevented failure.

---

## Timeline

Routine Inspection

↓

Lubrication Recommended

↓

Maintenance Delayed

↓

Bearing Temperature Increased

↓

High Vibration Observed

↓

Incident Occurred

↓

Emergency Shutdown

↓

Investigation

↓

Bearing Replacement

↓

Plant Restart

---

## Document Collection

Asset Register

Contains

- Asset Information
- Locations
- Install Dates

---

SOP Documents

SOP-01 Pump Maintenance

SOP-02 Motor Maintenance

SOP-03 Emergency Shutdown

---

Maintenance Logs

ML-001

Lubrication skipped

ML-002

Bearing noise

ML-003

Seal replacement

ML-004

Compressor inspection

---

Inspection Reports

INS-001

Bearing wear

INS-002

Oil contamination

INS-003

Motor inspection

---

Incident Report

INC-001

Pump failure

Emergency shutdown

Root Cause

Delayed maintenance

---

OEM Manual

Bearing limits

Lubrication interval

Operating parameters

---

Work Order

WO-001

Bearing replacement

Assigned Engineer

Completion details

---

Calibration Report

Pressure sensor calibration

---

Plant Layout

Simplified facility layout

---

## Knowledge Graph Design

Nodes

- Asset
- Engineer
- SOP
- Document
- Incident
- Inspection
- Maintenance Log

Relationships

Asset → FOLLOWS_SOP → SOP

Asset → REFERENCED_IN → Document

Engineer → MAINTAINED → Asset

Incident → CAUSED → Asset

Inspection → FOUND → Incident

Asset → CONNECTED_TO → Asset

---

## Demo Questions

Why did Pump P-101 fail?

Who serviced Pump P-101?

Show maintenance history.

Which SOP applies?

Which documents reference Pump P-101?

Why is bearing replacement recommended?

Compare Pump P-101 and Motor M-22.

---

## Asset Dashboard Data

Every asset should display

- Asset Information
- Health Status
- Intelligence Score
- Timeline
- Related Documents
- Related Assets
- AI Summary
- Maintenance Intelligence

---

## Naming Convention

Assets

P-101

M-22

C-07

SOP

SOP-01

SOP-02

Maintenance Logs

ML-001

Inspection Reports

INS-001

Incidents

INC-001

Work Orders

WO-001

---

## Dataset Folder Structure

sample-data/

assets/

maintenance/

inspection/

incident/

manuals/

work-orders/

layout/

generated-json/