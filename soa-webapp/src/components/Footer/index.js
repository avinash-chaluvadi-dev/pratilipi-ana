import React from 'react';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import LegatoLogo from 'static/images/legato-notag.png';
import Box from '@material-ui/core/Box';
import useStyles from './useStyles';
import globalStyles from 'styles';

const Sidebar = () => {
  const classes = useStyles();
  const globalClasses = globalStyles();

  return (
    <>
      <AppBar className={classes.appBar}>
        <Toolbar className={[globalClasses.flex, globalClasses.spaceBetween]}>
          <Box />
          <Box className={classes.text}>
            <Box>Powered by:</Box>
            <Box ml={2}>
              <img
                style={{ verticalAlign: 'middle' }}
                src={LegatoLogo}
                alt="Legato Logo"
              />
            </Box>
          </Box>
        </Toolbar>
      </AppBar>
    </>
  );
};

export default Sidebar;
