from sqlalchemy import Column, String, DateTime, Text, Float
from app.database.base import Base
from datetime import datetime, timezone
import uuid

class CopilotHistory(Base):
    __tablename__ = "copilot_history"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    confidence = Column(Float, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
