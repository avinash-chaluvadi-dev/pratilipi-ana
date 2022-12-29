import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';

import clsx from 'clsx';
import Drawer from '@material-ui/core/Drawer';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Avatar from '@material-ui/core/Avatar';
import IconButton from '@material-ui/core/IconButton';
import List from '@material-ui/core/List';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import Box from '@material-ui/core/Box';
import useStyles from './useStyles';
import globalStyles from 'styles';
import menu from './menu';
import mainLogo from 'static/images/main_logo.png';
import smallLogo from 'static/images/sml_logo.png';
import pratlipiLogo from 'static/images/voicemail.png';
import { useDispatch } from 'react-redux';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import SessionStorageService from 'api/sessionStorageService';
import { useHistory } from 'react-router-dom';

const Sidebar = ({ open, setOpen }) => {
  const classes = useStyles();
  const dispatch = useDispatch();
  const globalClasses = globalStyles();
  const sessionStorageService = SessionStorageService.getService();
  const [anchorEl, setAnchorEl] = useState(null);
  const logoutMenuOpen = Boolean(anchorEl);
  const history = useHistory();

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handMenu = () => {
    sessionStorageService.clearUserData();
    dispatch({
      type: 'LOGOUT_USER',
    });
    history.push('/login');
    window.location.reload(false);
    handleClose();
  };

  const openActionPopup = (index) => {
    dispatch({
      type: 'SWITCH_COMPONENTS',
      payload: { selectedItem: index },
    });
  };

  return (
    <>
      <AppBar
        position="fixed"
        className={clsx(classes.appBar, {
          [classes.appBarShift]: open,
        })}
      >
        <Toolbar className={[globalClasses.flex, globalClasses.spaceBetween]}>
          <Box className={classes.logoBox}>
            <img src={pratlipiLogo} width="200px" height="50px" alt="" />{' '}
            <Divider className={classes.divider} orientation="vertical" />
            <Typography className={classes.title}>
              Medicare Voicemail Messages
            </Typography>
          </Box>
          <Box />
          <Box className={classes.logoBoxRight}>
            <Box display="flex" flexDirection="column" mr={2}>
              <Typography variant="body1" className={globalClasses.mlAuto}>
                Welcome,
              </Typography>
              <Typography variant="body1" className={globalClasses.bold}>
                {sessionStorage.getItem('userName')}
              </Typography>
            </Box>
            <IconButton
              color="inherit"
              aria-label="Open drawer"
              edge="start"
              sixe="small"
              onClick={handleClick}
            >
              <Avatar></Avatar>
            </IconButton>
            <Menu
              id="basic-menu"
              anchorEl={anchorEl}
              open={logoutMenuOpen}
              onClose={handleClose}
              MenuListProps={{
                'aria-labelledby': 'basic-button',
              }}
            >
              <MenuItem onClick={handMenu}>Logout</MenuItem>
            </Menu>
          </Box>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        className={clsx(classes.drawer, {
          [classes.drawerOpen]: open,
          [classes.drawerClose]: !open,
        })}
        classes={{
          paper: clsx({
            [classes.drawerOpen]: open,
            [classes.drawerClose]: !open,
          }),
        }}
        onMouseEnter={() => setOpen(true)}
        onMouseLeave={() => setOpen(false)}
      >
        <Divider />
        <List>
          <Box mb={8}>
            <ListItem>
              {open ? (
                <>
                  <img src={mainLogo} alt="" />
                </>
              ) : (
                <img src={smallLogo} alt="" />
              )}
            </ListItem>
          </Box>
          {menu.map((item, index) => (
            <ListItem
              button
              key={index}
              component={NavLink}
              to={`/${Object.keys(item)[0].toLowerCase()}`}
              onClick={() => openActionPopup(index)}
              className={
                window.location.pathname.split('/')[1] ===
                Object.keys(item)[0].toLowerCase()
                  ? classes.sidebarMenuSelected
                  : classes.sidebarMenu
              }
            >
              <ListItemIcon className={globalClasses.textWhite}>
                {item[Object.keys(item)[0]]}
              </ListItemIcon>
              <ListItemText
                primary={Object.keys(item)[0]}
                className={globalClasses.textWhite}
              />
            </ListItem>
          ))}
        </List>
      </Drawer>
    </>
  );
};

export default Sidebar;
