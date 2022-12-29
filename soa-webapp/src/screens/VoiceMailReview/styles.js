import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  Card: {
    margin: '0px 0px -149px 0px',
    padding: '24px 12px 30px 24px',
    borderRadius: 16,
    boxShadow: '0 16px 32px 0 rgba(0, 0, 0, 0.1)',
    border: 'solid 1px rgba(0, 0, 0, 0.08)',
    backgroundColor: '#fff',
    width: '100%',
    height: '100%',
  },
  Card1: {
    padding: '24px 10px 0 10px',
    borderRadius: 16,
    boxShadow: '0 16px 32px 0 rgba(0, 0, 0, 0.1)',
    border: 'solid 1px rgba(0, 0, 0, 0.08)',
    backgroundColor: '#fff',
    width: '95%',
    height: '100%',
    marginBottom: 20,
    marginLeft: 10,
  },
  lsfInnerSubCardBox: {
    display: 'flex',
    alignItems: 'center',
  },
  textLeft: {
    textAlign: 'left',
    fontSize: 16,
    fontWeight: 'bold',
    width: 222,
  },
  subTextLeft: {
    textAlign: 'left',
    fontSize: 14,
    fontWeight: 'bold',
    marginLeft: '28px',
  },
  subTextRight: {
    textAlign: 'left',
    fontSize: 14,
    fontWeight: 'bold',
    marginLeft: '8px',
  },
  textAlignRight: {
    textAlign: 'right',
    fontWeight: 'bold',
    justifyContent: 'flex-end',
  },
  flexEnd: {
    justifyContent: 'flex-end',
  },
  sideCard: {
    textAlign: 'left',
    fontWeight: 'bold',
    justifyContent: 'flex-start',
  },
  textLeftFontSize: {
    textAlign: 'left',
    fontSize: 14,
    fontWeight: 'bold',
  },
  textLeftPadding: {
    fontSize: 16,
    // fontWeight: 'bold',
    padding: '0 20px',
  },
  textLeftPaddingBtn: {
    fontSize: 16,
    padding: '0 10px',
  },
  divider: {
    height: '15px',
    background: '#286ce2',
    marginRight: '10px',
    marginLeft: '10px',
    width: '1px!important',
  },
  dividerInvisible: {
    height: '15px',
    marginRight: '10px',
    marginLeft: '10px',
    width: '0px!important',
  },
  borderCls: {
    border: '1px solid #e9e9e9',
    padding: '8px 10px',
    fontSize: 16,
    borderRadius: 8,
    color: '#286ce2',
  },
  sortBorderCls: {
    padding: '8px 10px',
    fontSize: 16,
    borderRadius: 8,
    color: '#286ce2',
  },
  lsfInnerSubCard: {
    display: 'flex',
    alignItems: 'flex-start',
    justifyContent: 'space-between',
    '& .rmdp-container': {
      width: '100%',
    },
  },
  innerSubCard: {
    display: 'flex',
    alignItems: 'center',
    textAlign: 'left',
    justifyContent: 'space-between',
    fontSize: '16px',
    fontFamily: 'Lato',
    color: '#286ce2',
  },
  innerSubCardRed: {
    display: 'flex',
    alignItems: 'center',
    textAlign: 'left',
    justifyContent: 'space-between',
    fontSize: '16px',
    fontFamily: 'Lato',
    color: '#ff2236',
  },
  innerSubCardBold: {
    display: 'flex',
    alignItems: 'center',
    textAlign: 'left',
    justifyContent: 'space-between',
    fontSize: '16px',
    fontFamily: 'Lato',
    color: '#286ce2',
    fontWeight: 'bold',
  },
  subCard: {
    display: 'flex',
    alignItems: 'center',
    maxWidth: '98%',
  },
  Textbox: {
    width: '100%',
    height: '25px',
    padding: '4px 10px',
    borderRadius: 8,
    border: 'solid 1px #949494',
    backgroundColor: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
    fontFamily: 'Lato!important',
  },
  TextboxRound: {
    width: '100%',
    height: 30,
    padding: '4px 10px',
    borderRadius: 32,
    border: 'solid 1px #949494',
    backgroundColor: '#fff',
    fontSize: 16,
  },
  paddingLeftCls: {
    padding: '0 10px',
  },
  divBoxRound: {
    width: '35%',
    height: 30,
    borderRadius: 32,
    border: 'solid 1px #949494',
    backgroundColor: '#fff',
    fontSize: 16,
  },
  inputWithoutBorder: {
    border: 'none',
    width: '58%',
    fontSize: '14px',
    fontFamily: 'Lato',
    fontWeight: 'bold',
    margin: '0 7px 0 5px',
    color: '#1a191a',
    textAlign: 'center',
    '& :hover': {
      border: 'none',
    },
    '&:hover': {
      border: 'none',
    },
  },
  TextboxRoundRed: {
    width: '70px',
    height: 20,
    padding: '4px 13px',
    borderRadius: 32,
    border: 'solid 1px #ff2236',
    color: '#ff2236',
    fontSize: 16,
  },
  TextboxCopy: {
    width: '92%',
    height: 96,
    margin: '10px 0px 10px 0px',
    padding: '24.3px 10px 23.7px 10px',
    borderRadius: 8,
    border: 'solid 1px #949494',
    backgroundColor: '#fff',
    fontSize: 16,
    fontFamily: 'Lato!important',
  },
  disableCls: {
    pointerEvents: 'none',
    opacity: 0.5,
  },
  extensionCls: {
    borderRadius: '32px 0px 0px 31px',
    padding: '3px 10px 3px 10px',
    width: 100,
    background: '#EEE',
  },

  nodataTitle: {
    width: 400,
    height: 30,
    // margin: '364px 23px 9px 44px',
    fontFamily: 'Bitter',
    fontSize: 24,
    fontWeight: 'bold',
    lineHeight: 1.25,
    textAlign: 'center',
    color: '#666',
  },
  nodataPaddingTop: { padding: '5% 0' },
  nodataPaddingSides: { padding: '0 36%' },
  subTitleNodata: {
    width: 400,
    height: 44,
    // margin: '9px 0 24px 52px',
    fontFamily: 'Lato',
    fontSize: 16,
    fontWeight: 500,
    lineHeight: 1.38,
    textAlign: 'center',
    color: '#333',
  },
  snackbar: {
    '& .MuiSnackbar-anchorOriginBottomLeft': {
      bottom: '400px',
      left: '200px',
    },
  },
  reviewerCommentsContainer: {
    position: 'relative',
  },
  characterCount: {
    fontSize: '14px',
    position: 'absolute',
    bottom: '-10px',
    right: '3px',
  },
}));

export default useStyles;