from typing import List

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from sqlalchemy.orm import Session

from app.connectors.db_conn import get_db
from app.core.constants import (DATA_CONFLICT_MESSAGE, DATA_ERROR_LISTALL,
                                DATA_NOT_FOUND_MESSAGE, DB_ERROR,
                                DEFAULT_LIMIT_COUNT, DEFAULT_OFFSET_COUNT)
from app.core.exceptions import (InternalServerError, RecordAlreadyExists,
                                 RecordNotFound)
from app.schemas.models import VoicemailBox
from app.schemas.schemas import (ActionVoicemailBox, ActionVoicemailBoxUpdate,
                                 PaginatedVoicemailBox)
from app.utils import auth
from app.utils.utils import get_eastern_timezoneval

v1_router = APIRouter(tags=["voicemailbox"])

class VoicemailboxActions:
    def __init__(self):
        self.dataset = []

    def get_all_voicemailbox(
        self,
        session: Session,
        limit: int = DEFAULT_LIMIT_COUNT,
        offset: int = DEFAULT_OFFSET_COUNT,
    ) -> List[VoicemailBox]:
        ormqueryset = session.query(VoicemailBox).offset(offset).limit(limit).all()
        for item in ormqueryset:
            self.dataset.append({"vmb_id": item.vmb_id, "vmb_name": item.vmb_name})
        return self.dataset

    def create_voicemailbox(self, session: Session, voicemail_info: ActionVoicemailBox) -> VoicemailBox:
        voicemail_details = (
            session.query(VoicemailBox).filter(VoicemailBox.vmb_name == voicemail_info.vmb_name).first()
        )

        if voicemail_details is not None:
            raise RecordAlreadyExists
        final_data = dict((k, v) for k, v in voicemail_info.__dict__.items() if v!=None)
        new_voicemail_info = VoicemailBox(**final_data)
        new_voicemail_info.vmb_timestamp = get_eastern_timezoneval()
        session.add(new_voicemail_info)
        session.commit()
        session.refresh(new_voicemail_info)
        return new_voicemail_info

    def get_voicemailbox_info_by_id(self, session: Session, _id: int) -> VoicemailBox:
        voicemail_info = session.query(VoicemailBox).get(_id)
        if voicemail_info is None:
            raise RecordNotFound
        return voicemail_info

    def set_voicemailbox_info(self, session: Session, _id: int, info_update: ActionVoicemailBox) -> VoicemailBox:
        voicemail_info = self.get_voicemailbox_info_by_id(session, _id)
        if voicemail_info is None:
            raise RecordNotFound
        voicemail_info.vmb_name = info_update.vmb_name
        voicemail_info.vmb_status = info_update.vmb_status
        session.commit()
        session.refresh(voicemail_info)
        return voicemail_info

    def delete_voicemailbox_info(self, session: Session, _id: int):
        voicemail_info = self.get_voicemailbox_info_by_id(session, _id)
        if voicemail_info is None:
            raise RecordNotFound
        session.delete(voicemail_info)
        session.commit()
        return voicemail_info

@cbv(v1_router)
class Voicemailbox:
    """The following code base it imposes the routes of voicemail transaction table actions."""
    session: Session = Depends(get_db)
    @v1_router.get(
        "/list-voicemailbox", response_model=PaginatedVoicemailBox, dependencies=[Depends(auth.JWTBearer())]
    )
    def list_voicemail_box(self, limit: int = DEFAULT_LIMIT_COUNT, offset: int = DEFAULT_OFFSET_COUNT):
        try:
            obj_voicemail_actions = VoicemailboxActions()
            voicemail_list = obj_voicemail_actions.get_all_voicemailbox(self.session, limit, offset)
            return PaginatedVoicemailBox(limit=limit, offset=offset, data=voicemail_list)
        except RecordNotFound:
            raise RecordNotFound(message=DATA_ERROR_LISTALL)
        except Exception:
            raise InternalServerError(message=DB_ERROR)

    @v1_router.post("/add-voicemailbox", dependencies=[Depends(auth.JWTBearer())])
    def add_voicemail_box(self, voicemail_info: ActionVoicemailBoxUpdate):
        try:
            obj_voicemail_actions = VoicemailboxActions()
            voicemail_info = obj_voicemail_actions.create_voicemailbox(self.session, voicemail_info)
            return voicemail_info
        except RecordAlreadyExists:
            raise RecordAlreadyExists(message=DATA_CONFLICT_MESSAGE.format("voicemail box", voicemail_info.vmb_name))
        except Exception:
            raise InternalServerError(message=DB_ERROR)

    @v1_router.get("/get-voicemailbox", response_model=ActionVoicemailBox, dependencies=[Depends(auth.JWTBearer())])
    def get_voicemail_info(self, voicemail_id: int, session: Session = Depends(get_db)):
        try:
            obj_voicemail_actions = VoicemailboxActions()
            voicemail_info = obj_voicemail_actions.get_voicemailbox_info_by_id(session, voicemail_id)
            return ActionVoicemailBox(**voicemail_info.__dict__)
        except RecordNotFound:
            raise RecordNotFound(message=DATA_NOT_FOUND_MESSAGE.format("voicemail-box", voicemail_id))
        except RecordAlreadyExists:
            raise RecordAlreadyExists(message=DATA_CONFLICT_MESSAGE.format("voicemail-box", voicemail_id))
        except Exception:
            raise InternalServerError(message=DB_ERROR)

    @v1_router.put(
        "/set-voicemailbox", response_model=ActionVoicemailBoxUpdate, dependencies=[Depends(auth.JWTBearer())]
    )
    def update_voicemail(
        self, voicemail_id: int, new_info: ActionVoicemailBoxUpdate, session: Session = Depends(get_db)
    ):
        try:
            obj_voicemail_actions = VoicemailboxActions()
            voicemail_info = obj_voicemail_actions.set_voicemailbox_info(session, voicemail_id, new_info)
            return ActionVoicemailBox(**voicemail_info.__dict__)
        except RecordNotFound:
            raise RecordNotFound(message=DATA_NOT_FOUND_MESSAGE.format("voicemail-box", voicemail_id))
        except RecordAlreadyExists:
            raise RecordAlreadyExists(message=DATA_CONFLICT_MESSAGE.format("voicemail-box", voicemail_id))
        except Exception:
            raise InternalServerError(message=DB_ERROR)

    @v1_router.delete("/delete-voicemailbox", dependencies=[Depends(auth.JWTBearer())])
    def delete_voicemail(self, voicemail_id: int, session: Session = Depends(get_db)):
        try:
            obj_voicemail_actions = VoicemailboxActions()
            voicemail_info = obj_voicemail_actions.delete_voicemailbox_info(session, voicemail_id)
            return ActionVoicemailBox(**voicemail_info.__dict__)
        except RecordNotFound:
            raise RecordNotFound(message=DATA_NOT_FOUND_MESSAGE.format("voicemail-box", voicemail_id))
        except RecordAlreadyExists:
            raise RecordAlreadyExists(message=DATA_CONFLICT_MESSAGE.format("voicemail-box", voicemail_id))
        except Exception:
            raise RecordNotFound(message=DATA_NOT_FOUND_MESSAGE.format("voicemail-box", voicemail_id))