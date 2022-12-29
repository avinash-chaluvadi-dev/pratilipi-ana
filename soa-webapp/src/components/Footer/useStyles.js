import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  appBar: {
    position: 'relative',
    height: '64px',
    backgroundColor: theme.palette.common.white,
    boxShadow: 'none',
    top: '190px',
  },
  sidebarMenu: {
    color: theme.palette.common.white,
    borderLeft: '5px solid #1464DF',
  },
  sidebarMenuSelected: {
    color: theme.palette.common.white,
    borderLeft: '5px solid #ffffff',
  },
  text: {
    fontSize: '14px',
    fontFamily: 'Lato',
    color: theme.palette.common.muted,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
}));

export default useStyles;
