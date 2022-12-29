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
from app.schemas.models import VoicemailFeatures
from app.schemas.schemas import (ActionVoicemailFeaturesScm,
                                 PaginatedVoicemailFeaturesInfoScm)
from app.utils import auth
from app.utils.utils import get_eastern_timezoneval

v1_router = APIRouter(tags=["feature"])


class FeatureActions:
    def __init__(self):
        self.dataset = []

    def get_all_features(
        self,
        session: Session,
        limit: int = DEFAULT_LIMIT_COUNT,
        offset: int = DEFAULT_OFFSET_COUNT,
    ) -> List[VoicemailFeatures]:
        orm_query_set = session.query(VoicemailFeatures).offset(offset).limit(limit).all()
        for item in orm_query_set:
            self.dataset.append(
                {
                    "vmf_id": item.vmf_id,
                    "vmf_name": item.vmf_name,
                    "vmf_timestamp": item.vmf_timestamp,
                    "vmf_status": item.vmf_status,
                }
            )
        return self.dataset

    def create_feature(self, session: Session, feature_info: ActionVoicemailFeaturesScm) -> VoicemailFeatures:
        voicemail_details = (
            session.query(VoicemailFeatures).filter(VoicemailFeatures.vmf_name == feature_info.vmf_name).first()
        )
        if voicemail_details is not None:
            raise RecordAlreadyExists

        new_feature_info = VoicemailFeatures(**feature_info.dict())
        new_feature_info.vmf_timestamp = get_eastern_timezoneval()
        session.add(new_feature_info)
        session.commit()
        session.refresh(new_feature_info)
        return new_feature_info

    def get_features_info_by_id(self, session: Session, _id: int) -> VoicemailFeatures:
        feature_info = session.query(VoicemailFeatures).get(_id)
        if feature_info is None:
            raise RecordNotFound
        return feature_info

    def set_feature_info(
        self, session: Session, _id: int, info_update: ActionVoicemailFeaturesScm
    ) -> VoicemailFeatures:
        feature_info = self.get_features_info_by_id(session, _id)

        if feature_info is None:
            raise RecordNotFound

        feature_info.vmf_name = info_update.vmf_name
        feature_info.vmf_status = info_update.vmf_status
        session.commit()
        session.refresh(feature_info)

        return feature_info

    def delete_feature_info(self, session: Session, _id: int):
        feature_info = self.get_features_info_by_id(session, _id)

        if feature_info is None:
            raise RecordNotFound

        session.delete(feature_info)
        session.commit()
        return feature_info


@cbv(v1_router)
class Features:
    session: Session = Depends(get_db)

    @v1_router.get(
        "/list-features", response_model=PaginatedVoicemailFeaturesInfoScm, dependencies=[Depends(auth.JWTBearer())]
    )
    def list_voicemail_feature(self, limit: int = DEFAULT_LIMIT_COUNT, offset: int = DEFAULT_OFFSET_COUNT):
        try:
            obj_feature_actions = FeatureActions()
            voicemail_list = obj_feature_actions.get_all_features(self.session, limit, offset)
            return PaginatedVoicemailFeaturesInfoScm(limit=limit, offset=offset, data=voicemail_list)
        except RecordNotFound:
            raise RecordNotFound(message=DATA_ERROR_LISTALL)
        except Exception:
            raise InternalServerError(message=DB_ERROR)

    @v1_router.post("/add-feature", dependencies=[Depends(auth.JWTBearer())])
    def add_voicemail_feature(self, feature_info: ActionVoicemailFeaturesScm):
        try:
            obj_feature_actions = FeatureActions()
            feature_info = obj_feature_actions.create_feature(self.session, feature_info)
            return feature_info
        except RecordAlreadyExists:
            raise RecordAlreadyExists(message=DATA_CONFLICT_MESSAGE.format("feature", feature_info.vmf_name))
        except Exception:
            raise InternalServerError(message=DB_ERROR)

    @v1_router.get("/get-feature", response_model=ActionVoicemailFeaturesScm, dependencies=[Depends(auth.JWTBearer())])
    def get_feature_info(self, feature_id: int, session: Session = Depends(get_db)):
        try:
            obj_feature_actions = FeatureActions()
            feature_info = obj_feature_actions.get_features_info_by_id(session, feature_id)
            return ActionVoicemailFeaturesScm(**feature_info.__dict__)
        except RecordNotFound:
            raise RecordNotFound(message=DATA_NOT_FOUND_MESSAGE.format("voicemail-feature", feature_id))
        except RecordAlreadyExists:
            raise RecordAlreadyExists(message=DATA_CONFLICT_MESSAGE.format("voicemail-feature", feature_id))
        except Exception:
            raise InternalServerError(message=DB_ERROR)

    @v1_router.put("/set-feature", response_model=ActionVoicemailFeaturesScm, dependencies=[Depends(auth.JWTBearer())])
    def update_voicemail(
        self, feature_id: int, new_info: ActionVoicemailFeaturesScm, session: Session = Depends(get_db)
    ):
        try:
            obj_feature_actions = FeatureActions()
            feature_info = obj_feature_actions.set_feature_info(session, feature_id, new_info)
            return ActionVoicemailFeaturesScm(**feature_info.__dict__)
        except RecordNotFound:
            raise RecordNotFound(message=DATA_NOT_FOUND_MESSAGE.format("voicemail-feature", feature_id))
        except RecordAlreadyExists:
            raise RecordAlreadyExists(message=DATA_CONFLICT_MESSAGE.format("voicemail-feature", feature_id))
        except Exception:
            raise InternalServerError(message=DB_ERROR)

    @v1_router.delete("/delete-feature", dependencies=[Depends(auth.JWTBearer())])
    def delete_voicemail(self, feature_id: int, session: Session = Depends(get_db)):
        try:
            obj_feature_actions = FeatureActions()
            feature_info = obj_feature_actions.delete_feature_info(session, feature_id)
            return ActionVoicemailFeaturesScm(**feature_info.__dict__)
        except RecordNotFound:
            raise RecordNotFound(message=DATA_NOT_FOUND_MESSAGE.format("voicemail-feature", feature_id))
        except RecordAlreadyExists:
            raise RecordAlreadyExists(message=DATA_CONFLICT_MESSAGE.format("voicemail-feature", feature_id))
        except Exception:
            raise RecordNotFound(message=DATA_NOT_FOUND_MESSAGE.format("voicemail-feature", feature_id))
