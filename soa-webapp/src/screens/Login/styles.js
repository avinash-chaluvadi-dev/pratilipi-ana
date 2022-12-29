import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  loginForm: {
    width: '300px',
    marginBottom: '27px',
    '& .MuiOutlinedInput-root': {
      borderRadius: '8px',
      border: 'solid 0.8px #949494',
    },
    '& .MuiOutlinedInput-input': {
      fontSize: '14px',
      color: '#666666',
    },
  },
  loginFormError: {
    width: '300px',
    '& .MuiOutlinedInput-root': {
      borderRadius: '8px',
      border: 'solid 0.8px #949494',
    },
    '& .MuiOutlinedInput-input': {
      fontSize: '14px',
      color: '#666666',
    },
  },
  headerText: {
    fontSize: '24px',
    fontFamily: 'Bitter',
    fontWeight: 'medium!important',
    textAlign: 'left',
    color: '#333333',
  },
  bodyText: {
    fontSize: '14px',
    fontWeight: 'bold',
    lineHeight: '40px',
    textAlign: 'left',
    color: '#333333',
  },
  button: {
    textTransform: 'none',
    width: '300px',
    height: '40px',
    margin: '10px 0px 0px 0px',
    borderRadius: '8px',
    fontSize: '16px',
    fontFamily: 'Lato',
    fontWeight: 'bold',
    textAlign: 'center',
  },
  outerGrid: {
    minHeight: '90vh',
    width: '100%',
    overflow: 'hidden',
    alignItems: 'center',
    justifyContent: 'center',
  },
  divider: {
    marginTop: '5vh',
    height: '30vh',
  },
  outerBox: {
    display: 'flex',
    alignItems: 'center',
    width: 'fit-content',
  },
  logoBox: {
    marginTop: '40px',
    marginRight: '100px',
  },
  errorText: {
    fontSize: '12px',
    color: '#d20a3c',
    alignItems: 'center',
    display: 'flex',
  },
}));

export default useStyles;
