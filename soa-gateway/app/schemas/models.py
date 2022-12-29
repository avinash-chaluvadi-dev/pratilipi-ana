import enum
from datetime import datetime
from enum import unique

from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Enum

from app.utils.utils import get_eastern_timezoneval

# gen-base
Base = declarative_base()


# voice-mail-extraction-states
class TransactionStates(str, enum.Enum):
    Downloaded = "Downloaded"
    Transcribed = "Transcribed"
    Processed = "Processed"


# voice-mail-extraction-states
class ReviewStatus(str, enum.Enum):
    Pending = "Pending"
    InProgress = "InProgress"
    Completed = "Completed"
    Overdue = "Overdue"


# voicemail_features
class VoicemailFeatures(Base):
    """Database model structure for voicemail_features table"""

    __tablename__ = "voicemail_features"
    vmf_id = Column(Integer, primary_key=True, index=True)
    vmf_name = Column(String(255))
    vmf_timestamp = Column(DateTime, default=get_eastern_timezoneval())
    vmf_status = Column(Boolean, default=False)


# voicemail_box
class VoicemailBox(Base):
    """Database model structure for voicemail_box table"""

    __tablename__ = "voicemail_box"

    vmb_id = Column(Integer, primary_key=True, index=True)
    vmb_name = Column(String(255))
    vmb_timestamp = Column(DateTime, default=get_eastern_timezoneval())
    vmb_status = Column(Boolean, default=False)
    voice_mails = relationship(
        "VoicemailTransaction", secondary="voicemail_relations", back_populates="voicemail_boxes"
    )


# voicemail_transaction vmb:vmt
class VoicemailTransaction(Base):
    """Database model structure for voicemail_transaction table"""

    __tablename__ = "voicemail_transaction"
    vm_id = Column(Integer, primary_key=True, index=True)
    vm_uuid = Column(String(250), unique=True)
    vm_name = Column(String(255), default=None)
    vm_member_name = Column(String(255), default=None)
    vm_audio_url = Column(String(1000), default=None)
    vm_system_state = Column(Enum(TransactionStates), nullable=False, default=TransactionStates.Downloaded.value)
    vm_review_state = Column(Enum(ReviewStatus), nullable=False, default=ReviewStatus.Pending.value)
    vm_timestamp = Column(DateTime, default=get_eastern_timezoneval())
    vm_active_status = Column(Boolean, default=False)
    vm_ner = Column(JSON, default={"entities": []})
    vm_call_reason = Column(JSON, default={"reason": []})
    vm_call_duration = Column(String(100), default=None)
    vm_member_called_back = Column(Boolean, default=False)
    vm_callback_no_reachable = Column(Boolean, default=False)
    vm_callback_no = Column(String(20), default=None)
    vm_extension_id = Column(String(255), default=None)
    vm_transcript_dtls = Column(String(5000), default=None)
    vm_normalized_dtls = Column(String(5000), default=None)
    vm_reviewer_name = Column(String(250), default=None)
    vm_review_start_date = Column(DateTime, nullable=True, default=None)
    vm_review_end_date = Column(DateTime, nullable=True, default=None)
    vm_reviewer_comments = Column(String(200), default=None)
    voicemail_boxes = relationship("VoicemailBox", secondary="voicemail_relations", back_populates="voice_mails")
    vm_is_overdue = Column(Boolean, default=False)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class VoicemailRelations(Base):
    """Database model structure for voicemail_relations table"""

    __tablename__ = "voicemail_relations"

    voicemail_transaction_id = Column(Integer, ForeignKey("voicemail_transaction.vm_id"), primary_key=True)
    voicemail_box_id = Column(Integer, ForeignKey("voicemail_box.vmb_id"), primary_key=True)


class VoicemailTransactionArchive(Base):
    """Database model structure for voicemail_transaction_archive table"""

    __tablename__ = "voicemail_transaction_archive"
    id = Column(Integer, primary_key=True, index=True)
    vm_id = Column(Integer)
    vm_uuid = Column(String(250), default=None)
    vm_name = Column(String(255), default=None)
    vm_member_name = Column(String(255), default=None)
    vm_audio_url = Column(String(1000), default=None)
    vm_system_state = Column(Enum(TransactionStates))
    vm_review_state = Column(Enum(ReviewStatus))
    vm_timestamp = Column(DateTime, default=get_eastern_timezoneval())
    vm_active_status = Column(Boolean, default=False)
    vm_ner = Column(JSON, default={})
    vm_call_reason = Column(JSON, default={})
    vm_call_duration = Column(String(100), default=None)
    vm_member_called_back = Column(Boolean, default=False)
    vm_callback_no_reachable = Column(Boolean, default=False)
    vm_callback_no = Column(String(20), default=None)
    vm_extension_id = Column(String(255), default=None)
    vm_transcript_dtls = Column(String(5000), default=None)
    vm_normalized_dtls = Column(String(5000), default=None)
    vm_reviewer_name = Column(String(250), default=None)
    vm_review_start_date = Column(DateTime, nullable=True, default=None)
    vm_review_end_date = Column(DateTime, nullable=True, default=None)
    vm_reviewer_comments = Column(String(200), default=None)
    vm_is_overdue = Column(Boolean, default=False)
