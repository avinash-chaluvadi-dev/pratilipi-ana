import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import MuiPagination from '@material-ui/lab/Pagination';
import useStyles from 'components/Pagination/styles';

const Pagination = withStyles({
  root: {
    '& .MuiPaginationItem-icon': {
      backgroundColor: 'inherit',
      fontSize: 14,
    },
  },
})(MuiPagination);

export default function PaginationComponent(props) {
  const { page, handleChangePagination, totalrecords } = props;
  const classes = useStyles();

  const handleChange = (event, value) => {
    handleChangePagination(event, value);
  };

  return (
    <div className={classes.root}>
      <Pagination
        count={totalrecords}
        page={page}
        onChange={handleChange}
        color="primary"
      />
    </div>
  );
}
