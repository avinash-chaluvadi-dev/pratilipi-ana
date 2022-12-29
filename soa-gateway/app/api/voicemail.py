import datetime
from io import BytesIO
from typing import List

import pandas as pd
import sqlalchemy as db
from sqlalchemy import JSON, desc, func
from sqlalchemy.orm import Session

from app.connectors.db_conn import get_db, get_engine
from app.core.constants import (
    DATA_CONFLICT_MESSAGE,
    DATA_ERROR_LISTALL,
    DATA_NOT_FOUND_MESSAGE,
    DB_ERROR,
    DEFAULT_LIMIT_COUNT,
    DEFAULT_OFFSET_COUNT,
    EXCEL_REPORT_ERROR,
    EXPORT_REPORT_COLUMNS,
    GENERIC_FORBIDDEN_ERROR,
    INVALID_NER_ENTRY,
    NOT_ACCEPTABLE_ERROR,
    RECEIVED_TIME,
    REQUEST_TIMEOUT_ERROR,
    SORTLIST,
    STATE_FILTER,
    STATUS_FILTER,
    UNAUTHORISED_ERROR_MESSAGE,
    VOICEMAIL_SET_ERROR,
    PROTEGRITY_MAPPING,
)
from app.core.exceptions import (
    BadRequestException,
    ForbiddenException,
    GenerateReportException,
    InternalServerError,
    NotAcceptableError,
    RecordAlreadyExists,
    RecordNotFound,
    RequestTimeoutError,
    UnauthorisedError,
)
from app.schemas.models import (
    ReviewStatus,
    TransactionStates,
    VoicemailBox,
    VoicemailRelations,
    VoicemailTransaction,
)
from app.schemas.schemas import (
    ActionVoicemailTransactionScm,
    ActionVoicemailTransactionUpdateScm,
    PaginatedVoicemailTransactionInfoScm,
    VoicemailTransactionScm,
)
from app.utils import auth
from app.utils.protegrity import ProtegrityConfigurationUtils
from app.utils.utils import get_eastern_timezoneval, query_to_dict
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from fastapi_utils.cbv import cbv
from app.core.config import settings

v1_router = APIRouter(tags=["voicemail"])


class VoicemailActions:
    """The following class indicates the voicemail transaction table crud action."""

    def __init__(self):
        self.dataset = []

    def get_voicemail_info_by_id(self, session: Session, _id: int) -> VoicemailTransaction:
        voicemail_info = session.query(VoicemailTransaction).get(_id)
        if voicemail_info is None:
            raise RecordNotFound
        required_dict = prep_tokenize_data(voicemail_info)
        detokenize_response = ProtegrityConfigurationUtils(required_dict).detokenization()
        return prep_detokenize_data(detokenize_response[0], voicemail_info)

    def get_voicemail_info_by_uuid(self, session: Session, uuid: str) -> VoicemailTransaction:
        voicemail_info = session.query(VoicemailTransaction).filter_by(vm_uuid=uuid).one()

        if voicemail_info is None:
            raise RecordNotFound
        required_dict = prep_tokenize_data(voicemail_info)

        detokenize_response = ProtegrityConfigurationUtils(required_dict).detokenization()

        return prep_detokenize_data(detokenize_response[0], voicemail_info)

    def voicemail_sorting(self, sort, orm_query_set):
        if sort == SORTLIST[0]:
            orm_query_set = orm_query_set.order_by(desc(VoicemailTransaction.vm_member_name))
        elif sort == SORTLIST[1]:
            orm_query_set = orm_query_set.order_by(desc(VoicemailTransaction.vm_call_reason.cast(JSON)["reason"]))
        elif sort == SORTLIST[2]:
            orm_query_set = orm_query_set.order_by(desc(VoicemailTransaction.vm_callback_no))
        elif sort == SORTLIST[3]:
            orm_query_set = orm_query_set.order_by(desc(VoicemailTransaction.vm_timestamp))
        return orm_query_set

    def voicemail_main_filter(
        self,
        voicemail_box,
        date_end,
        date_start,
        time_start,
        time_end,
        orm_query_set,
        filterapplied,
    ):
        if voicemail_box != 0:
            # box-filer:
            orm_query_set = orm_query_set.filter(VoicemailRelations.voicemail_box_id == voicemail_box)
            filterapplied = 1
        if date_end != "" and date_start != "":
            orm_query_set = orm_query_set.filter(
                func.DATE(VoicemailTransaction.vm_timestamp) >= date_start,
                func.DATE(VoicemailTransaction.vm_timestamp) <= date_end,
            )
            filterapplied = 1
        if time_start != "" and time_end != "":
            orm_query_set = orm_query_set.filter(
                func.TIME(VoicemailTransaction.vm_timestamp) >= time_start,
                func.TIME(VoicemailTransaction.vm_timestamp) <= time_end,
            )
            filterapplied = 1

        return [filterapplied, orm_query_set]

    def voicemail_review_state_filter(self, state, orm_query_set, sort):
        if state in STATE_FILTER:
            orm_query_set = orm_query_set.filter(VoicemailTransaction.vm_review_state == state)
            if sort.strip() == "":
                if state == STATE_FILTER[1]:
                    orm_query_set = orm_query_set.order_by(desc(VoicemailTransaction.vm_review_start_date))
                elif state == STATE_FILTER[2]:
                    orm_query_set = orm_query_set.order_by(desc(VoicemailTransaction.vm_review_end_date))
                else:
                    orm_query_set = orm_query_set.order_by(desc(VoicemailTransaction.vm_timestamp))
        elif state.strip() != "":
            return []
        return orm_query_set

    """ Function to get list of voicemail info with filter and sort features """

    def get_all_voicemail(
        self,
        session: Session,
        limit: int,
        offset: int,
        sort: str,
        date_start: str,
        date_end: str,
        time_start: str,
        time_end: str,
        voicemail_box: int,
        download_excel: bool,
        state: str,
    ) -> List[VoicemailTransaction]:
        orm_query_set = (
            session.query(VoicemailTransaction)
            .join(VoicemailRelations)
            .join(VoicemailBox)
            .filter(VoicemailBox.vmb_id == VoicemailRelations.voicemail_box_id)
        )
        if orm_query_set is None:
            raise RecordNotFound
        filterapplied = 0
        orm_query_set = self.voicemail_sorting(sort, orm_query_set)
        filterapplied, orm_query_set = self.voicemail_main_filter(
            voicemail_box,
            date_end,
            date_start,
            time_start,
            time_end,
            orm_query_set,
            filterapplied,
        )

        # Excel:
        if download_excel:
            sqldataframe = pd.DataFrame(query_to_dict(orm_query_set))
            return [sqldataframe, True]
        total_count = orm_query_set.count()
        overdue_count = orm_query_set.filter(VoicemailTransaction.vm_review_state == STATUS_FILTER[0]).count()
        pending_count = orm_query_set.filter(VoicemailTransaction.vm_review_state == STATUS_FILTER[1]).count()
        in_progress_count = orm_query_set.filter(VoicemailTransaction.vm_review_state == STATUS_FILTER[2]).count()
        completed_count = orm_query_set.filter(VoicemailTransaction.vm_review_state == STATUS_FILTER[3]).count()
        orm_query_set = self.voicemail_review_state_filter(state, orm_query_set, sort)
        status_counts = {
            "total_count": total_count,
            "overdue_count": overdue_count,
            "pending_count": pending_count,
            "in_progress_count": in_progress_count,
            "completed_count": completed_count,
        }
        if orm_query_set == []:
            return [orm_query_set, status_counts]
        if filterapplied == 0:
            orm_query_set = orm_query_set.limit(limit).offset(offset).all()
        else:
            orm_query_set = orm_query_set.limit(limit).offset(offset)
        data_list = []
        for query_data in orm_query_set:
            data_list.append(prep_tokenize_data(query_data))
        detokenize_response_temp = ProtegrityConfigurationUtils(data_list).detokenization()

        for item in orm_query_set:
            for data_query in detokenize_response_temp:

                if item.vm_id == data_query[0][0]["id"]:
                    prep_detokenize_data(data_query[0], item)

                    self.dataset.append(
                        {
                            "vm_id": item.vm_id,
                            "vmb_name": item.voicemail_boxes[0].vmb_name,
                            "vm_uuid": item.vm_uuid,
                            "vm_name": item.vm_name,
                            "vm_audio_url": "{0}{1}{2}".format(settings.AUDIO_DNS, "?file=", item.vm_audio_url),
                            "vm_system_state": item.vm_system_state,
                            "vm_review_state": item.vm_review_state,
                            "vm_member_name": item.vm_member_name,
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
                            "vm_member_called_back": item.vm_member_called_back,
                            "vm_callback_no_reachable": item.vm_callback_no_reachable,
                            "vm_call_duration": item.vm_call_duration,
                            "vm_is_overdue": item.vm_is_overdue,
                        }
                    )

        return [self.dataset, status_counts]

    """ Function to delete the voicemail info """

    def delete_voicemail_info(self, session: Session, _id: int):
        voicemail_info = self.get_voicemail_info_by_id(session, _id)
        if voicemail_info is None:
            raise RecordNotFound
        session.delete(voicemail_info)
        session.commit()
        return voicemail_info

    """ Function to create the voicemail info """

    def create_voicemail(
        self,
        session: Session,
        voicemail_info: ActionVoicemailTransactionScm,
        voicemail_box_name,
    ) -> VoicemailTransaction:
        """Function to add a new voicemail info to the database"""
        voice_box = session.query(VoicemailBox).filter(VoicemailBox.vmb_name == voicemail_box_name).first()
        if voice_box is None:
            raise RecordNotFound
        else:
            prepped_data = prep_tokenize_data(voicemail_info)
            tokenize_response = ProtegrityConfigurationUtils(prepped_data).tokenization()
            voicemail_info = prep_detokenize_data(tokenize_response[0], voicemail_info)

            voicemail_details = (
                session.query(VoicemailTransaction)
                .filter(VoicemailTransaction.vm_name.like(voicemail_info.vm_name))
                .filter(VoicemailTransaction.vm_uuid.like(voicemail_info.vm_uuid))
            ).first()
            if voicemail_details is not None:
                raise RecordAlreadyExists

            final_data = dict((k, v) for k, v in voicemail_info.__dict__.items() if v is not None)
            new_voicemail_info = VoicemailTransaction(**final_data)
            if not final_data.get("vm_timestamp"):
                new_voicemail_info.vm_timestamp = get_eastern_timezoneval()
            session.add(new_voicemail_info)
            session.commit()
            finaldata = new_voicemail_info
            new_voicemail_info.voicemail_boxes = [voice_box]
            session.commit()
            session.refresh(new_voicemail_info)
            return finaldata

    def set_voicemail_info(
        self,
        session: Session,
        uuid: str,
        info_update: ActionVoicemailTransactionUpdateScm,
    ) -> VoicemailTransaction:
        """Function to update voicemail info to the database"""
        voicemail_info = self.get_voicemail_info_by_uuid(session, uuid)
        if voicemail_info is None:
            raise RecordNotFound
        else:
            info_update_dict = info_update.__dict__
            final_dict = dict((k, v) for k, v in info_update_dict.items() if v is not None)
            if final_dict.get("vm_review_state") == "InProgress":
                final_dict["vm_review_start_date"] = get_eastern_timezoneval()
            elif final_dict.get("vm_review_state") == "Completed":
                final_dict["vm_review_end_date"] = get_eastern_timezoneval()
            voicemail_info.update(**final_dict)
            voicemail_vm_name = voicemail_info.vm_name
            required_dict = prep_tokenize_data(voicemail_info)
            tokenize_response = ProtegrityConfigurationUtils(required_dict).tokenization()
            voicemail_info = prep_detokenize_data(tokenize_response[0], voicemail_info)
            session.commit()
            session.refresh(voicemail_info)
            voicemail_info.vm_name = voicemail_vm_name.upper()
            return voicemail_info


@cbv(v1_router)
class Voicemails:
    """The following code base it imposes the routes of voicemail transaction table actions."""

    session: Session = Depends(get_db)

    @v1_router.get(
        "/list-voicemails",
        response_model=PaginatedVoicemailTransactionInfoScm,
        dependencies=[Depends(auth.JWTBearer())],
    )
    def list_voicemail(
        self,
        limit: int = DEFAULT_LIMIT_COUNT,
        offset: int = DEFAULT_OFFSET_COUNT,
        sort: str = "",
        date_start: str = "",
        date_end: str = "",
        time_start: str = "",
        time_end: str = "",
        voicemail_box: int = 0,
        download_excel: bool = False,
        state: str = "",
    ):
        """API to get the list of voicemail info sort"""
        try:
            obj_voicemail_actions = VoicemailActions()
            (voicemail_list, status_counts,) = obj_voicemail_actions.get_all_voicemail(
                self.session,
                limit,
                offset,
                sort,
                date_start,
                date_end,
                time_start,
                time_end,
                voicemail_box,
                download_excel,
                state,
            )
            if download_excel:
                try:
                    output = BytesIO()
                    detokenize_voicemail_list = download_excel_data(voicemail_list)
                    detokenize_voicemail_list.to_excel(output, index=True)
                    output.seek(0)
                    headers = {
                        "Content-Disposition": 'attachment; filename="voicemail_transaction_report_'
                        + str(datetime.datetime.now())
                        + '.xlsx"'
                    }
                    return StreamingResponse(output, headers=headers)
                except Exception:
                    raise GenerateReportException(message=EXCEL_REPORT_ERROR)

            return PaginatedVoicemailTransactionInfoScm(
                offset=offset,
                limit=limit,
                sort=sort,
                date_start=date_start,
                date_end=date_end,
                time_start=time_start,
                time_end=time_end,
                voicemail_box=voicemail_box,
                data=voicemail_list,
                status=status_counts,
                download_excel=download_excel,
                state=state,
            )
        except RecordNotFound:
            raise RecordNotFound(message=DATA_ERROR_LISTALL)
        except UnauthorisedError:
            raise UnauthorisedError(message=UNAUTHORISED_ERROR_MESSAGE)
        except NotAcceptableError:
            raise NotAcceptableError(message=NOT_ACCEPTABLE_ERROR)
        except RequestTimeoutError:
            raise RequestTimeoutError(message=REQUEST_TIMEOUT_ERROR)
        except ForbiddenException:
            raise ForbiddenException(message=GENERIC_FORBIDDEN_ERROR)
        except Exception as err:
            raise InternalServerError(message=str(err))

    @v1_router.post("/add-voicemail", dependencies=[Depends(auth.JWTBearer())])
    def add_voicemail(
        self,
        voicemail_info: ActionVoicemailTransactionScm,
        voicemail_box_name: str,
    ):
        try:
            obj_voicemail_actions = VoicemailActions()
            voicemail_info = obj_voicemail_actions.create_voicemail(self.session, voicemail_info, voicemail_box_name)
            return ActionVoicemailTransactionScm(**voicemail_info.__dict__)
        except RecordNotFound:
            raise RecordNotFound(message=DATA_NOT_FOUND_MESSAGE.format("voicemail-box", voicemail_box_name))
        except RecordAlreadyExists:
            raise RecordAlreadyExists(message=DATA_CONFLICT_MESSAGE.format("voicemail", voicemail_info.vm_uuid))
        except UnauthorisedError:
            raise UnauthorisedError(message=UNAUTHORISED_ERROR_MESSAGE)
        except NotAcceptableError:
            raise NotAcceptableError(message=NOT_ACCEPTABLE_ERROR)
        except RequestTimeoutError:
            raise RequestTimeoutError(message=REQUEST_TIMEOUT_ERROR)
        except ForbiddenException:
            raise ForbiddenException(message=GENERIC_FORBIDDEN_ERROR)
        except BadRequestException:
            raise BadRequestException(message=INVALID_NER_ENTRY)
        except Exception as err:
            raise InternalServerError(message=str(err))

    @v1_router.get(
        "/get-voicemail",
        response_model=ActionVoicemailTransactionScm,
        dependencies=[Depends(auth.JWTBearer())],
    )
    def get_voicemail_info(self, voicemail_uuid: str):
        try:
            obj_voicemail_actions = VoicemailActions()
            voicemail_info = obj_voicemail_actions.get_voicemail_info_by_uuid(self.session, voicemail_uuid)
            return ActionVoicemailTransactionScm(**voicemail_info.__dict__)
        except RecordNotFound:
            raise RecordNotFound(message=DATA_NOT_FOUND_MESSAGE.format("voicemail", voicemail_uuid))
        except RecordAlreadyExists:
            raise RecordAlreadyExists(message=DATA_CONFLICT_MESSAGE.format("voicemail", voicemail_uuid))
        except UnauthorisedError:
            raise UnauthorisedError(message=UNAUTHORISED_ERROR_MESSAGE)
        except NotAcceptableError:
            raise NotAcceptableError(message=NOT_ACCEPTABLE_ERROR)
        except RequestTimeoutError:
            raise RequestTimeoutError(message=REQUEST_TIMEOUT_ERROR)
        except ForbiddenException:
            raise ForbiddenException(message=GENERIC_FORBIDDEN_ERROR)
        except Exception as erro:
            raise InternalServerError(message=str(erro))

    @v1_router.put(
        "/set-voicemail",
        response_model=ActionVoicemailTransactionUpdateScm,
        dependencies=[Depends(auth.JWTBearer())],
    )
    def update_voicemail(
        self,
        voicemail_uuid: str,
        info_update: ActionVoicemailTransactionUpdateScm,
    ):
        try:
            obj_voicemail_actions = VoicemailActions()
            voicemail_info = obj_voicemail_actions.set_voicemail_info(self.session, voicemail_uuid, info_update)
            return ActionVoicemailTransactionUpdateScm(**voicemail_info.__dict__)
        except RecordNotFound:
            raise RecordNotFound(message=DATA_NOT_FOUND_MESSAGE.format("voicemail", voicemail_uuid))
        except RecordAlreadyExists:
            raise RecordAlreadyExists(message=DATA_CONFLICT_MESSAGE.format("voicemail", voicemail_uuid))
        except UnauthorisedError:
            raise UnauthorisedError(message=UNAUTHORISED_ERROR_MESSAGE)
        except NotAcceptableError:
            raise NotAcceptableError(message=NOT_ACCEPTABLE_ERROR)
        except RequestTimeoutError:
            raise RequestTimeoutError(message=REQUEST_TIMEOUT_ERROR)
        except ForbiddenException:
            raise ForbiddenException(message=GENERIC_FORBIDDEN_ERROR)
        except BadRequestException:
            raise BadRequestException(message=INVALID_NER_ENTRY)
        except InternalServerError:
            raise InternalServerError(message=DB_ERROR)

    @v1_router.delete("/delete-voicemail", dependencies=[Depends(auth.JWTBearer())])
    def delete_voicemail(self, voicemail_id: int):
        try:
            obj_voicemail_actions = VoicemailActions()
            voicemail_info = obj_voicemail_actions.delete_voicemail_info(self.session, voicemail_id)
            return ActionVoicemailTransactionScm(**voicemail_info.__dict__)
        except RecordNotFound:
            raise RecordNotFound(message=DATA_NOT_FOUND_MESSAGE.format("voicemail", voicemail_id))
        except RecordAlreadyExists:
            raise RecordAlreadyExists(message=DATA_CONFLICT_MESSAGE.format("voicemail", voicemail_id))
        except Exception:
            raise RecordNotFound(message=DATA_NOT_FOUND_MESSAGE.format("voicemail", voicemail_id))


def prepare_ner_transcript_data(voicemail_info, required_dict):
    if voicemail_info.vm_ner and len(voicemail_info.vm_ner) > 0:
        if "entities" not in voicemail_info.vm_ner:
            raise BadRequestException
        entity_list = [item["entity"] for item in voicemail_info.vm_ner["entities"]]
        required_dict["lastName"] = entity_list
    if voicemail_info.vm_transcript_dtls and len(voicemail_info.vm_transcript_dtls.strip()) > 0:
        required_dict["B64_ENCRYPTION"] = voicemail_info.vm_transcript_dtls


def prep_tokenize_data(data: ActionVoicemailTransactionScm) -> list:
    tokens = []
    token_mapping = {}
    token_mapping1 = {}

    if hasattr(data, "vm_id"):
        token_mapping["id"] = data.vm_id
        token_mapping1["id"] = data.vm_id

    for key, value in PROTEGRITY_MAPPING.items():

        if hasattr(data, key):
            if key == "vm_normalized_dtls":
                token_mapping1[value] = getattr(data, key)
                token_mapping1["normalized"] = True
            else:
                token_mapping[value] = getattr(data, key)

    if data.vm_ner:
        if "entities" not in data.vm_ner:
            raise BadRequestException
        entity_list = [item["entity"] for item in data.vm_ner["entities"]]
        token_mapping["lastName"] = entity_list

    tokens.append([token_mapping, token_mapping1])
    return tokens


def prep_detokenize_data(data: list, obj: ActionVoicemailTransactionScm) -> ActionVoicemailTransactionScm:

    for d in data:
        if "Name" in d:
            obj.vm_name = d["Name"]
        if "firstName" in d:
            obj.vm_member_name = d["firstName"]
        if "SSN" in d:
            obj.vm_callback_no = d["SSN"]
        if "OtherID" in d:
            obj.vm_extension_id = d["OtherID"]
        if "lastName" in d:
            for i, item in enumerate(d["lastName"]):
                obj.vm_ner["entities"][i]["entity"] = item
        if "B64_ENCRYPTION" in d:
            if "normalized" in d:
                obj.vm_normalized_dtls = d["B64_ENCRYPTION"]
            else:
                obj.vm_transcript_dtls = d["B64_ENCRYPTION"]

    return obj


def update_row(row):
    row["vm_member_called_back"] = "YES" if row["vm_member_called_back"] else "NO"
    row["vm_callback_no_reachable"] = "YES" if row["vm_callback_no_reachable"] else "NO"
    row["vm_call_reason"] = row["vm_call_reason"]["reason"] if row["vm_call_reason"].get("reason") else "N/A"
    row["vm_is_overdue"] = "YES" if row["vm_is_overdue"] else "NO"


def download_excel_data(voicemail_list):
    data_list = []
    voicemail_list = voicemail_list.reset_index()
    for index, row in voicemail_list.iterrows():
        data_dict = dict()
        data_dict["id"] = row["vm_id"]
        data_list.append(prep_tokenize_data(row))
    detokenize_response_temp = ProtegrityConfigurationUtils(data_list).detokenization()
    final_df_list = []
    for index, row in voicemail_list.iterrows():
        for data_query in detokenize_response_temp:
            if row["vm_id"] == data_query[0][0]["id"]:
                prep_detokenize_data(data_query[0], row)
                update_row(row)
                df_data = [
                    row["voicemail_boxes"],
                    row["vm_uuid"],
                    row["vm_name"],
                    row["vm_timestamp"].strftime("%m/%d/%Y"),
                    row["vm_timestamp"].strftime("%H:%M:%S"),
                    row["vm_transcript_dtls"],
                    row["vm_member_name"],
                    row["vm_extension_id"],
                    row["vm_review_state"].value,
                    row["vm_callback_no"],
                    row["vm_call_reason"],
                    row["vm_member_called_back"],
                    row["vm_callback_no_reachable"],
                    row["vm_call_duration"],
                    row["vm_reviewer_name"],
                    row["vm_reviewer_comments"],
                    row["vm_review_start_date"],
                    row["vm_review_end_date"],
                    row["vm_is_overdue"],
                ]
                final_df_list.append(df_data)
    detokenize_voicemail_list = pd.DataFrame(final_df_list, columns=EXPORT_REPORT_COLUMNS)
    detokenize_voicemail_list.index.names = ["Slno"]
    detokenize_voicemail_list.index = detokenize_voicemail_list.index + 1

    return detokenize_voicemail_list
