import { makeStyles } from '@material-ui/core/styles';

const MMDPUseStyles = makeStyles((theme) => ({
  datepicker: {
    width: '10px',
    borderRadius: '8px',
    boxShadow: '0 2px 4px 0 rgba(0, 0, 0, 0.08)',
    border: 'solid 1px #eaeaea',
    backgroundColor: '#fff',
    zIndex: 999,
  },
  btnGroup: {
    padding: '256px 0 14px 0',
    margin: '0 0 0 238px',
  },

  applyBtnCls: {
    width: '107px',
    height: '30px',
    margin: '5px',
    borderRadius: '8px',
    fontSize: '14px',
    fontWeight: 'bold',
    textTransform: 'none',
  },

  customCls: {
    '& .react-datepicker': {
      '& .month-container': {
        padding: '71px 0px',
      },
    },
    '& .react-datepicker__month-container': {
      padding: '71px 0px',
    },
    '&.month-container': {
      padding: '71px 0px',
    },
  },

  inputBoxCls: {
    width: '100%!important',
    '& .MuiOutlinedInput-input': {
      padding: '0px 15px',
      color: '#286ce2',
      fontSize: '14px',
      fontWeight: 'bold',
      fontFamily: 'Lato',
      textAlign: 'left',
    },
    '& .MuiOutlinedInput-adornedEnd': {
      paddingRight: '1px',
      borderRadius: '8px',
      fontSize: '14px',
      height: '38px',
    },
    '& .MuiOutlinedInput-notchedOutline': {
      border: 'solid 1px #949494',
    },
  },
}));

export default MMDPUseStyles;
