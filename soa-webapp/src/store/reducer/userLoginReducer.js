import { updateObject } from 'utils/utility';

const initialState = {
  userAuthenticated: false,
  userAuthenticationError: false,
  accessToken: '',
  refreshToken: '',
  userName: '',
  userId: '',
};

let auth = sessionStorage.getItem('userAuthenticated');
initialState.userAuthenticated = auth ? auth : false;
initialState.accessToken = sessionStorage.getItem('accessToken');
initialState.refreshToken = sessionStorage.getItem('refreshToken');
initialState.userName = sessionStorage.getItem('userName');
initialState.userId = sessionStorage.getItem('userId');

export default function userLoginReducer(state = initialState, action = {}) {
  switch (action.type) {
    case 'AUTHENTICATE_USER_LOGIN_SUCCESS':
      sessionStorage.setItem('userAuthenticated', true);
      sessionStorage.setItem('accessToken', action.response.access_token);
      sessionStorage.setItem('refreshToken', action.response.refresh_token);
      sessionStorage.setItem('userName', action.response.display_name);
      sessionStorage.setItem('userId', action.response.cn);
      return updateObject(state, {
        authenticationMessage: action.response.message,
        userAuthenticated: true,
        userAuthenticationError: false,
        accessToken: action.response.access_token,
        refreshToken: action.response.refresh_token,
        userName: action.response.display_name,
        userId: action.response.cn,
      });
    case 'AUTHENTICATE_USER_LOGIN_ERROR':
    case 'AUTHENTICATE_USER_LOGIN_PROMISEERROR':
      return updateObject(state, {
        authenticationMessage: action.response,
        userAuthenticationError: true,
      });
    case 'LOGOUT_USER':
      return updateObject(state, {
        userAuthenticated: false,
        userAuthenticationError: false,
        accessToken: '',
        refreshToken: '',
        userName: '',
        userId: '',
      });

    default:
      return state;
  }
}
