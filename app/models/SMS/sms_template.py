
from sqlalchemy import Column, Integer, String, SmallInteger
from app.core.database import Base


class SMSTemplate(Base):
    __tablename__ = "sms_templates"

    id = Column(SmallInteger, primary_key=True, index=True, autoincrement=True)
    pe_id = Column(String(32), nullable=False)
    dlt_template_id = Column(String(32), nullable=False)
    name = Column(String(255), nullable=False)
    sender_id = Column(String(6), nullable=False)
    content = Column(String(1000), nullable=False)
    text_type = Column(String(10), nullable=False, default="uni")
    is_active = Column(Integer, nullable=False, default=1)