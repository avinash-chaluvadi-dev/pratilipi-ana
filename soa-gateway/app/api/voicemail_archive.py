from typing import List

from sqlalchemy.orm import Session

from app.connectors.db_conn import get_db
from app.core.constants import (
    DATA_ERROR_LISTALL,
    DATA_NOT_FOUND_MESSAGE,
    DB_ERROR,
    DEFAULT_LIMIT_COUNT,
    DEFAULT_OFFSET_COUNT,
)
from app.core.exceptions import InternalServerError, RecordNotFound
from app.schemas.models import VoicemailTransactionArchive
from app.schemas.schemas import ActionVoicemailTransactionArchiveScm, PaginatedVoicemailArchiveTransactionInfoScm
from app.utils import auth
from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

v1_router = APIRouter(tags=["voicemail_archive"])


class VoicemailActionsArchive:

    """The following class indicates the voicemail archive transaction table crud action."""

    def __init__(self):
        self.dataset = []

    # Function to get list of voicemail_archive info
    def get_all_voicemail_archive(
        self, session: Session, limit: int = DEFAULT_LIMIT_COUNT, offset: int = DEFAULT_OFFSET_COUNT,
    ) -> List[VoicemailTransactionArchive]:
        ormqueryset = session.query(VoicemailTransactionArchive).offset(offset).limit(limit).all()
        for item in ormqueryset:
            self.dataset.append(
                {
                    "vm_uuid": item.vm_uuid,
                    "vm_name": item.vm_name,
                    "vm_member_name": item.vm_member_name,
                    "vm_audio_url": item.vm_audio_url,
                    "vm_system_state": item.vm_system_state,
                    "vm_review_state": item.vm_review_state,
                    "vm_active_status": item.vm_active_status,
                    "vm_timestamp": item.vm_timestamp,
                    "vm_ner": item.vm_ner,
                    "vm_call_reason": item.vm_call_reason,
                    "vm_callback_no": item.vm_callback_no,
                    "vm_extension_id": item.vm_extension_id,
                    "vm_transcript_dtls": item.vm_transcript_dtls,
                    "vm_normalized_dtls": item.vm_normalized_dtls,
                    "vm_reviewer_name": item.vm_reviewer_name,
                    "vm_review_start_date": item.vm_review_start_date,
                    "vm_review_end_date": item.vm_review_end_date,
                    "vm_reviewer_comments": item.vm_reviewer_comments,
                }
            )
        return self.dataset

    def get_voicemail_archive_info_by_id(self, session: Session, _id: int) -> VoicemailTransactionArchive:
        voicemail_archive_info = session.query(VoicemailTransactionArchive).get(_id)

        if voicemail_archive_info is None:
            raise RecordNotFound

        return voicemail_archive_info


@cbv(v1_router)
class VoicemailsArchive:
    session: Session = Depends(get_db)

    @v1_router.get(
        "/list-voicemails-archive",
        response_model=PaginatedVoicemailArchiveTransactionInfoScm,
        dependencies=[Depends(auth.JWTBearer())],
    )
    def list_voicemail(
        self, limit: int = DEFAULT_LIMIT_COUNT, offset: int = DEFAULT_OFFSET_COUNT,
    ):
        try:
            obj_voicemail_actions = VoicemailActionsArchive()
            voicemail_list = obj_voicemail_actions.get_all_voicemail_archive(self.session, limit, offset)
            return PaginatedVoicemailArchiveTransactionInfoScm(offset=offset, limit=limit, data=voicemail_list)
        except RecordNotFound:
            raise RecordNotFound(message=DATA_ERROR_LISTALL)
        except Exception:
            raise InternalServerError(message=DB_ERROR)

    @v1_router.get(
        "/voicemail-archive/",
        response_model=ActionVoicemailTransactionArchiveScm,
        dependencies=[Depends(auth.JWTBearer())],
    )
    def get_voicemail_archive_info(self, voicemail_id: int):
        try:
            obj_voicemail_actions = VoicemailActionsArchive()
            voicemail_archive_info = obj_voicemail_actions.get_voicemail_archive_info_by_id(self.session, voicemail_id)
            return ActionVoicemailTransactionArchiveScm(**voicemail_archive_info.__dict__)
        except RecordNotFound:
            raise RecordNotFound(message=DATA_NOT_FOUND_MESSAGE.format("voicemail-archive", voicemail_id))
        except Exception:
            raise InternalServerError(message=DB_ERROR)
