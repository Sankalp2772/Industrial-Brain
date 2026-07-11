from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional

class NodeType(str, Enum):
    ASSET = "Asset"
    DOCUMENT = "Document"
    ENGINEER = "Engineer"
    INSPECTION = "Inspection"
    INCIDENT = "Incident"
    MAINTENANCE_LOG = "MaintenanceLog"
    SOP = "SOP"
    WORK_ORDER = "WorkOrder"
    OEM_MANUAL = "OEMManual"
    DEPARTMENT = "Department"

class RelationshipType(str, Enum):
    CONNECTED_TO = "CONNECTED_TO"
    MAINTAINED_BY = "MAINTAINED_BY"
    REFERENCED_IN = "REFERENCED_IN"
    MENTIONS = "MENTIONS"
    FOLLOWS_SOP = "FOLLOWS_SOP"
    CAUSED = "CAUSED"
    FOUND_IN = "FOUND_IN"
    FIXES = "FIXES"

class DocumentNode(BaseModel):
    id: str = Field(description="Unique identifier for the document")
    type: str = Field(description="The type of the document (e.g. SOP, Asset Register, etc.)")

class AssetNode(BaseModel):
    id: str = Field(description="Unique identifier for the asset")
    name: str = Field(description="Name of the asset")
    type: str = Field(description="Type of the asset")

class EngineerNode(BaseModel):
    id: str = Field(description="Unique identifier or name of the engineer")
    name: str = Field(description="Name of the engineer")
    department: Optional[str] = Field(None, description="Department the engineer belongs to")

class MaintenanceActionNode(BaseModel):
    id: str = Field(description="Unique identifier for the maintenance action")
    action_taken: str = Field(description="Description of the maintenance action taken")
    date: Optional[str] = Field(None, description="Date of the maintenance action")

class InspectionFindingNode(BaseModel):
    id: str = Field(description="Unique identifier for the inspection finding")
    finding: str = Field(description="Description of the finding")
    severity: Optional[str] = Field(None, description="Severity of the finding")

class IncidentNode(BaseModel):
    id: str = Field(description="Unique identifier for the incident")
    description: str = Field(description="Description of the incident")
    date: Optional[str] = Field(None, description="Date of the incident")

class Relationship(BaseModel):
    source_id: str = Field(description="ID of the source node")
    source_type: NodeType = Field(description="Type of the source node")
    target_id: str = Field(description="ID of the target node")
    target_type: NodeType = Field(description="Type of the target node")
    relationship_type: RelationshipType = Field(description="Type of the relationship")

class KnowledgeObject(BaseModel):
    document: DocumentNode
    assets: List[AssetNode] = Field(default_factory=list)
    engineers: List[EngineerNode] = Field(default_factory=list)
    maintenance_actions: List[MaintenanceActionNode] = Field(default_factory=list)
    inspection_findings: List[InspectionFindingNode] = Field(default_factory=list)
    incidents: List[IncidentNode] = Field(default_factory=list)
    relationships: List[Relationship] = Field(default_factory=list)
