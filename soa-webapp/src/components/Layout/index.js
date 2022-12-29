import React from 'react';
import clsx from 'clsx';
import Sidebar from 'components/Sidebar';
import { Box } from '@material-ui/core';
import useStyles from './useStyles';
import globalStyles from 'styles';

const Layout = ({ children }) => {
  const [open, setOpen] = React.useState(false);

  const classes = useStyles();
  const globalClasses = globalStyles();
  return (
    <Box className={globalClasses.bgLight}>
      <Sidebar open={open} setOpen={setOpen} />
      <Box
        className={clsx(classes.mainContent, {
          [classes.mainContentShift]: open,
        })}
      >
        {children}
      </Box>
    </Box>
  );
};

export default Layout;
