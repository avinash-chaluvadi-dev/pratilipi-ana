import jwt from 'jwt-decode';

const SessionStorageService = (function () {
  var _service;
  function _getService() {
    if (!_service) {
      _service = this;
      return _service;
    }
    return _service;
  }
  function _setToken(tokenObj) {
    sessionStorage.setItem('accessToken', tokenObj.access_token);
    sessionStorage.setItem('refreshToken', tokenObj.refresh_token);
  }
  function _getAccessToken() {
    return sessionStorage.getItem('accessToken');
  }
  function _getRefreshToken() {
    return sessionStorage.getItem('refreshToken');
  }
  function _clearAccessToken() {
    sessionStorage.removeItem('accessToken');
  }
  function _clearToken() {
    sessionStorage.removeItem('accessToken');
    sessionStorage.removeItem('refreshToken');
  }
  function _clearUserData() {
    sessionStorage.removeItem('accessToken');
    sessionStorage.removeItem('refreshToken');
    sessionStorage.removeItem('userAuthenticated');
    sessionStorage.removeItem('userName');
    sessionStorage.removeItem('userId');
  }
  function _accessTokenExpiryCheck(accessToken) {
    const decodedAccessToken = jwt(accessToken);
    if (Math.floor(Date.now() / 1000) >= decodedAccessToken['exp']) {
      return true;
    }
    return false;
  }

  function _refreshTokenExpiryCheck(refreshToken) {
    const decodedRefreshToken = jwt(refreshToken);
    if (Math.floor(Date.now() / 1000) > decodedRefreshToken['exp']) {
      return true;
    }
    return false;
  }
  return {
    getService: _getService,
    setToken: _setToken,
    getAccessToken: _getAccessToken,
    getRefreshToken: _getRefreshToken,
    clearAccessToken: _clearAccessToken,
    clearToken: _clearToken,
    clearUserData: _clearUserData,
    accessTokenExpiryCheck: _accessTokenExpiryCheck,
    refreshTokenExpiryCheck: _refreshTokenExpiryCheck,
  };
})();
export default SessionStorageService;
