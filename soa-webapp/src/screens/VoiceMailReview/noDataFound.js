import React from 'react';
import { Grid, Typography } from '@material-ui/core';
import useStyles from './styles';
import NoDataFoundcImg from 'static/images/notDataFound_1.png';

const NoDataFound = ({ selectedtab }) => {
  const classes = useStyles();
  const getStatus = () => {
    if (selectedtab === 4) {
      return 'Overdue';
    } else if (selectedtab === 3) {
      return 'Completed';
    } else if (selectedtab === 2) {
      return 'In Progress';
    } else {
      return 'Pending';
    }
  };

  return (
    <Grid xs={12} item className={classes.nodataPaddingTop}>
      <img src={NoDataFoundcImg} alt="" width="146px" height="146px" />
      <Grid xs={12} item className={classes.nodataPaddingSides}>
        <Typography className={classes.nodataTitle}>
          {' '}
          No {getStatus()} Voicemail(s) available
        </Typography>
        <Typography className={classes.subTitleNodata}>
          Change the date, time and voicemail box to view the voicemails to review
        </Typography>
      </Grid>
    </Grid>
  );
};
export default NoDataFound;
