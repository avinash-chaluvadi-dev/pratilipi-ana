/* This API wrapper is useful because it:
   1. Centralizes our Axios default configuration.
   2. Abstracts away the logic for determining the baseURL.
   3. Provides a clear, easily consumable list of JavaScript functions
      for interacting with the API. This keeps API calls short and consistent. 
*/

import { http } from './config';
import { CommonResponse } from 'store/action/types';

const loadeFunStart = (dispatch) => {
  dispatch({
    type: 'START_LOADER',
    payload: { isLoader: true },
  });
};
const loadeFunStop = (dispatch) => {
  dispatch({
    type: 'STOP_LOADER',
    payload: { isLoader: false },
  });
};

const SUCCESSSTATUS = [200, 201, 204];
export const post = async (dispatch, url, data, types) => {
  try {
    loadeFunStart(dispatch);
    dispatch({
      type: types + '_' + CommonResponse['INIT'],
    });
    const response = await http.post(url, data);
    dispatchResponse(dispatch, response, types);
  } catch (e) {
    errorHandler(e, dispatch, url, types);
  }
};

export const get = async (dispatch, url, types, params) => {
  try {
    loadeFunStart(dispatch);

    const response = await http.get(url, { params: params });
    dispatchResponse(dispatch, response, types);
  } catch (e) {
    errorHandler(e, dispatch, url, types);
  }
};

export const put = async (dispatch, url, data, types, params) => {
  try {
    loadeFunStart(dispatch);

    const response = await http.put(url, data, { params: params });
    dispatchResponse(dispatch, response, types);
  } catch (e) {
    errorHandler(e, dispatch, url, types);
  }
};

export const remove = async (dispatch, url, types) => {
  try {
    loadeFunStart(dispatch);

    dispatch({
      type: types + '_' + CommonResponse['INIT'],
    });
    const response = await http.delete(url);
    dispatchResponse(dispatch, response, types);
  } catch (e) {
    errorHandler(e, dispatch, url, types);
  }
};

export const patch = async (dispatch, url, data, types) => {
  try {
    loadeFunStart(dispatch);

    dispatch({
      type: types + '_' + CommonResponse['INIT'],
    });
    const response = await http.patch(url, data);
    dispatchResponse(dispatch, response, types);
  } catch (e) {
    errorHandler(e, dispatch, url, types);
  }
};

export const dispatchResponse = async (dispatch, response, types) => {
  try {
    if (SUCCESSSTATUS.includes(response.status)) {
      dispatch({
        type: types + '_' + CommonResponse['SUCCESS'],
        response: await response.data,
      });
      loadeFunStop(dispatch);
    } else {
      dispatch({
        type: types + '_' + CommonResponse['ERROR'],
        response: await response.data,
      });
      loadeFunStop(dispatch);
    }
  } catch (e) {
    dispatch({
      type: types + '_' + CommonResponse['PROMISEERROR'],
      response: await response.data,
    });
    loadeFunStop(dispatch);

    return e;
  }
};

const errorHandler = (e, dispatch, url, types) => {
  if (!e.status) {
    alert('Something is Broken ......  Kindly Refresh the Page and Continue !!');
    dispatch({
      type: types + '_' + CommonResponse['PROMISEERROR'],
      response: { status: 500 },
    });
    loadeFunStop(dispatch);
    return;
  }
  dispatch({
    type: CommonResponse['PROMISEERROR'] + '_' + types,
    response: e,
  });
  loadeFunStop(dispatch);

  return e;
};

const APIService = {
  get,
  post,
  put,
  remove,
  patch,
};
export default APIService;
