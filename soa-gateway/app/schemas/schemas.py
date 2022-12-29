import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, constr

from app.schemas.models import ReviewStatus, TransactionStates
from app.utils.utils import get_eastern_timezoneval
from app.core.constants import REVIEWER_COMMENTS_LIMIT


# voicemail-transaction:
# To support creation and update APIs
class ActionVoicemailTransactionScm(BaseModel):
    vm_uuid: str
    vm_name: str
    vm_audio_url: Optional[str]
    vm_system_state: Optional[TransactionStates]
    vm_review_state: Optional[ReviewStatus]
    vm_active_status: Optional[bool]
    vm_member_name: Optional[str]
    vm_ner: Optional[dict]
    vm_timestamp: Optional[datetime] = Field(None, nullable=True)
    vm_call_reason: Optional[dict]
    vm_callback_no: Optional[str]
    vm_extension_id: Optional[str]
    vm_transcript_dtls: Optional[str]
    vm_normalized_dtls: Optional[str]
    vm_reviewer_name: Optional[str]
    vm_reviewer_comments: Optional[str]
    vm_call_duration: Optional[str]
    vm_member_called_back: Optional[bool]
    vm_callback_no_reachable: Optional[bool]
    vm_is_overdue: Optional[bool]


class VoicemailTransactionScm(ActionVoicemailTransactionScm):
    id: int

    class Config:
        orm_mode: True


class ActionVoicemailTransactionUpdateScm(BaseModel):
    vm_uuid: Optional[str]
    vm_name: Optional[str]
    vm_system_state: Optional[TransactionStates]
    vm_review_state: Optional[ReviewStatus]
    vm_active_status: Optional[bool]
    vm_member_name: Optional[str]
    vm_ner: Optional[dict]
    vm_call_reason: Optional[dict]
    vm_callback_no: Optional[str]
    vm_extension_id: Optional[str]
    vm_transcript_dtls: Optional[str]
    vm_normalized_dtls: Optional[str]
    vm_reviewer_name: Optional[str]
    vm_reviewer_comments: Optional[constr(max_length=REVIEWER_COMMENTS_LIMIT)]
    vm_call_duration: Optional[str]
    vm_member_called_back: Optional[bool]
    vm_callback_no_reachable: Optional[bool]


class VoicemailSort(str, enum.Enum):
    member_name = "membername"
    reasoncall = "reasoncall"
    callnumber = "callnumber"
    receivedtime = "receivedtime"


# To support list cars API
class PaginatedVoicemailTransactionInfoScm(BaseModel):
    limit: int
    offset: int
    sort: Optional[str] = Field(None, nullable=True)
    date_start: Optional[str] = Field(None, nullable=True)
    date_end: Optional[str] = Field(None, nullable=True)
    time_start: Optional[str] = Field(None, nullable=True)
    time_end: Optional[str] = Field(None, nullable=True)
    voicemail_box: Optional[int] = Field(None, nullable=True)
    download_excel: Optional[bool]
    state: Optional[str] = Field(None, nullable=True)
    data: list
    status: dict


# voicemail-feature:
# TO support creation and update APIs
class ActionVoicemailFeaturesScm(BaseModel):
    vmf_name: str
    vmf_status: bool


class VoicemailFeaturesScm(ActionVoicemailFeaturesScm):
    id: int

    class Config:
        orm_mode: True


# To support list cars API
class PaginatedVoicemailFeaturesInfoScm(BaseModel):
    limit: int
    offset: int
    data: list


class ActionVoicemailBox(BaseModel):
    vmb_name: str
    vmb_id: int
    vmb_status: bool


class ActionVoicemailBoxUpdate(BaseModel):
    vmb_name: Optional[str]
    vmb_status: Optional[bool]


class VoicemailBoxes(ActionVoicemailBox):
    id: int

    class Config:
        orm_mode: True


class PaginatedVoicemailBox(BaseModel):
    limit: int
    offset: int
    data: list


class ActionVoicemailTransactionArchiveScm(BaseModel):
    vm_uuid: str
    vm_name: str
    vm_member_name: str
    vm_audio_url: str
    vm_system_state: TransactionStates
    vm_review_state: ReviewStatus
    vm_active_status: bool
    vm_ner: dict
    vm_call_reason: dict
    vm_callback_no: str
    vm_extension_id: str
    vm_transcript_dtls: str
    vm_normalized_dtls: str
    vm_reviewer_name: str
    vm_reviewer_comments: str
    vm_call_duration = str
    vm_member_called_back = bool
    vm_callback_no_reachable = bool


class VoicemailTransactionArchiveScm(ActionVoicemailTransactionArchiveScm):
    id: int

    class Config:
        orm_mode: True


class PaginatedVoicemailArchiveTransactionInfoScm(BaseModel):
    limit: int
    offset: int
    data: list
