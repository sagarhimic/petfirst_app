from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Numeric,
    Index
)
from app.core.database import Base

class SMSTemplate(Base):
    __tablename__ = "sms_templates"

    id = Column(Integer, primary_key=True, index=True)
    pe_id = Column(String(32), nullable=True)
    dlt_template_id = Column(String(32), nullable=True)
    name = Column(String(125), nullable=True)
    sender_id = Column(String(6), nullable=True)
    content = Column(String(1000), nullable=True)
    text_type = Column(String(10), nullable=True, index=True)
    is_active = Column(Integer, nullable=True)
