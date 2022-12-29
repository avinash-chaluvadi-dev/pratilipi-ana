import { VoiceMailReview } from './types';
import service from 'api/service';

export const voiceMailReviewAction = (params) => (dispatch) => {
  service.get(
    dispatch,
    `/list-voicemails`,
    VoiceMailReview['VOICE_MAIL_REVIEW'],
    params
  );
};

export const voiceMailBox = (params) => (dispatch) => {
  service.get(
    dispatch,
    `/list-voicemailbox`,
    VoiceMailReview['VOICE_MAIL_BOX'],
    params
  );
};

export const reasonForCall = (params) => (dispatch) => {
  service.get(
    dispatch,
    `/list-features`,
    VoiceMailReview['REASON_FOR_CALL'],
    params
  );
};

export const voiceMailReviewStatsAction = () => (dispatch) => {
  service.get(
    dispatch,
    `/get-voicemail-status`,
    VoiceMailReview['VOICE_MAIL_REVIEW_STAT']
  );
};

export const updateVoiceMail = (body, params) => (dispatch) => {
  service.put(
    dispatch,
    `/set-voicemail`,
    body,
    VoiceMailReview['VOICE_MAIL_UPDATE'],
    params
  );
};

export const downloadReport = (params) => (dispatch) => {
  service.get(
    dispatch,
    `/list-voicemails`,
    VoiceMailReview['VOICE_MAIL_REVIEW_DOWNLOAD'],
    params
  );
};
