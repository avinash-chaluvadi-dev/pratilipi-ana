import axios from 'axios';
import SessionStorageService from './sessionStorageService';
import { Redirect } from 'react-router-dom';
import { Envurl } from 'Envurl';
let envData = Envurl();
export const downloadBaseUrl = envData;
export const http = axios.create({
  baseURL: envData,
});

// SessionStorageService
const sessionStorageService = SessionStorageService.getService();

// Add a request interceptor
http.interceptors.request.use(
  async (config) => {
    config.headers['Content-Type'] = 'application/json';
    const accessToken = sessionStorageService.getAccessToken();
    if (accessToken) {
      const isAccessTokenExpired =
        sessionStorageService.accessTokenExpiryCheck(accessToken);
      if (!isAccessTokenExpired) {
        config.headers['Authorization'] = 'Bearer ' + accessToken;
      } else {
        sessionStorageService.clearAccessToken();
        const refreshToken = sessionStorageService.getRefreshToken();
        const isRefreshTokenExpired =
          sessionStorageService.refreshTokenExpiryCheck(refreshToken);
        if (!isRefreshTokenExpired) {
          return await http
            .post('/auth/refresh', {
              refresh_token: refreshToken,
            })
            .then((res) => {
              if (res.status === 200) {
                sessionStorageService.setToken(res.data);
                const updatedAccessToken = sessionStorageService.getAccessToken();
                config.headers['Authorization'] = 'Bearer ' + updatedAccessToken;
                return config;
              }
            });
        } else {
          sessionStorageService.clearUserData();
          window.location.reload(false);
        }
      }
    }
    return config;
  },
  (error) => {
    Promise.reject(error);
  }
);

//Add a response interceptor
http.interceptors.response.use(
  (response) => {
    return response;
  },
  function (error) {
    const originalRequest = error.config;

    if (
      error.response.status === 400 &&
      originalRequest.url === `${envData}/auth/refresh`
    ) {
      sessionStorageService.clearUserData();
      return <Redirect to="/login" />;
    }

    return Promise.reject(error);
  }
);
