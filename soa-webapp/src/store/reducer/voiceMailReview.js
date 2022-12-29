const initialState = {
  voiceMailReviewResult: [],
  voiceMailReviewStatsResult: {},
  voiceMailBoxList: [],
  reasonForCallList: [],
  voiceMailUpdateRes: {},
  downloadReportRes: '',
  totalrecords: 0,
};
export default function voiceMailReducer(state = initialState, action = {}) {
  switch (action.type) {
    case 'VOICE_MAIL_REVIEW_SUCCESS':
      return {
        ...state,
        voiceMailReviewResult: action?.response?.data,
        totalrecords: action?.response?.status?.total_count,
        voiceMailReviewStatsResult: action?.response.status,
      };
    case 'REASON_FOR_CALL_SUCCESS':
      return { ...state, reasonForCallList: action?.response?.data };
    case 'VOICE_MAIL_BOX_SUCCESS':
      return { ...state, voiceMailBoxList: action?.response?.data };
    case 'VOICE_MAIL_REVIEW_STAT_SUCCESS':
      return {
        ...state,
        voiceMailReviewStatsResult: action?.response.status,
      };
    case 'VOICE_MAIL_UPDATE_SUCCESS':
      return {
        ...state,
        voiceMailUpdateRes: action?.response,
      };
    case 'VOICE_MAIL_REVIEW_DOWNLOAD_SUCCESS':
      return {
        ...state,
        downloadReportRes: action?.response,
      };
    default:
      return state;
  }
}
