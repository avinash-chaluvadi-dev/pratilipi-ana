import { combineReducers } from 'redux';
import userLoginReducer from 'store/reducer/userLoginReducer';
import loaderReducer from 'store/reducer/loaderReducer';
import voiceMailReducer from 'store/reducer/voiceMailReview';

const appReducer = combineReducers({
  // bringin your reducers here
  userLoginReducer,
  loaderReducer,
  voiceMailReducer,
});

export default appReducer;
