import React, { useState, useEffect } from 'react';
import Box from '@material-ui/core/Box';
import Grid from '@material-ui/core/Grid';
import Divider from '@material-ui/core/Divider';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import FormHelperText from '@mui/material/FormHelperText';
import logo from 'static/images/legato-no-tag.svg';
import useStyles from './styles';
import OutlinedInput from '@mui/material/OutlinedInput';
import InputAdornment from '@mui/material/InputAdornment';
import FormControl from '@mui/material/FormControl';
import Visibility from 'static/images/iconography-system-visible.svg';
import VisibilityOff from 'static/images/iconography-system-invisible.svg';
import ClearIcon from '@mui/icons-material/Clear';
import IconButton from '@mui/material/IconButton';
import { useSelector, useDispatch } from 'react-redux';
import { userLogin } from 'store/action/login';
import { useHistory } from 'react-router-dom';

const Login = () => {
  const { userAuthenticated, userAuthenticationError } = useSelector(
    (state) => state.userLoginReducer
  );
  const [id, setId] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const loginCls = useStyles();
  const dispatch = useDispatch();
  const history = useHistory();

  useEffect(() => {
    if (userAuthenticated) {
      dispatch({
        type: 'STOP_LOADER',
        payload: { isLoader: false },
      });
      history.push('/voicemail');
    }
  }, [userAuthenticated, history, dispatch]);

  useEffect(() => {
    if (userAuthenticationError) {
      dispatch({
        type: 'STOP_LOADER',
        payload: { isLoader: false },
      });
    }
  }, [userAuthenticationError, dispatch]);

  const onFormSubmit = (e) => {
    e.preventDefault();
    let formData = {
      username: id,
      password: password,
    };
    dispatch(userLogin(formData));
    dispatch({
      type: 'START_LOADER',
      payload: { isLoader: true },
    });
  };

  return (
    <Grid container direction="column" className={loginCls.outerGrid}>
      <Grid item lg={10} md={20} xs={10}>
        <Box className={loginCls.outerBox}>
          <Box className={loginCls.logoBox}>
            <img src={logo} alt="Upload" />
          </Box>
          <Divider className={loginCls.divider} orientation="vertical" />
          <Box ml={10} component="form" autoComplete="off" onSubmit={onFormSubmit}>
            <FormControl className={loginCls.loginForm}>
              <Typography className={loginCls.headerText}>Log In</Typography>
              <Typography>&nbsp;</Typography>
              <Typography className={loginCls.bodyText}>
                Anthem Domain ID*
              </Typography>
              {userAuthenticationError ? (
                <FormControl required={true} error variant="standard">
                  <OutlinedInput
                    size="small"
                    className={loginCls.loginFormError}
                    placeholder="Enter anthem domain id"
                    value={id}
                    onChange={(e) => setId(e.target.value)}
                  />
                  <FormHelperText className={loginCls.errorText}>
                    <ClearIcon />
                    Please enter a valid anthem domain id
                  </FormHelperText>
                </FormControl>
              ) : (
                <FormControl required={true} variant="standard">
                  <OutlinedInput
                    size="small"
                    className={loginCls.loginForm}
                    placeholder="Enter anthem domain id"
                    value={id}
                    onChange={(e) => setId(e.target.value)}
                  />
                </FormControl>
              )}
              <Typography className={loginCls.bodyText}>Password*</Typography>
              {userAuthenticationError ? (
                <FormControl error variant="standard" required={true}>
                  <OutlinedInput
                    size="small"
                    className={loginCls.loginFormError}
                    helperText="Incorrect entry."
                    type={showPassword ? 'text' : 'password'}
                    placeholder="Enter password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    endAdornment={
                      <InputAdornment position="end">
                        <IconButton
                          onClick={(e) => setShowPassword(!showPassword)}
                          onMouseDown={(event) => event.preventDefault()}
                          edge="end"
                        >
                          {showPassword ? (
                            <img src={Visibility} alt="Visbility off" />
                          ) : (
                            <img src={VisibilityOff} alt="Visbility on" />
                          )}
                        </IconButton>
                      </InputAdornment>
                    }
                  />
                  <FormHelperText className={loginCls.errorText}>
                    <ClearIcon />
                    Please enter a valid password
                  </FormHelperText>
                </FormControl>
              ) : (
                <FormControl required={true}>
                  <OutlinedInput
                    size="small"
                    className={loginCls.loginForm}
                    helperText="Incorrect entry."
                    type={showPassword ? 'text' : 'password'}
                    placeholder="Enter password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    endAdornment={
                      <InputAdornment position="end">
                        <IconButton
                          onClick={(e) => setShowPassword(!showPassword)}
                          onMouseDown={(event) => event.preventDefault()}
                          edge="end"
                        >
                          {showPassword ? (
                            <img src={Visibility} alt="Visbility off" />
                          ) : (
                            <img src={VisibilityOff} alt="Visbility on" />
                          )}
                        </IconButton>
                      </InputAdornment>
                    }
                  />
                </FormControl>
              )}
            </FormControl>
            <Typography>
              <Button
                variant="contained"
                color="primary"
                size="large"
                type="submit"
                className={loginCls.button}
              >
                Log In
              </Button>
            </Typography>
          </Box>
        </Box>
      </Grid>
    </Grid>
  );
};

export default Login;
