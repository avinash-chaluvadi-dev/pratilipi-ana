import { makeStyles } from '@material-ui/core/styles';
import arrowLeft from 'static/images/arrowLeft.svg';
import arrowRight from 'static/images/arrowRight.svg';

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      marginTop: theme.spacing(2),
      fontSize: 14,
    },

    '& ul > li:not(:first-child):not(:last-child) > button:not(.Mui-selected)': {
      backgroundColor: '#f7f7f7',
      color: '#286ce2',
    },
    '& .Mui-selected': {
      backgroundColor: '#286ce2',
      color: '#fff',
    },
    '& .MuiPagination-ul': {
      '& > li:first-child': {
        '& button': {
          color: '#286ce2 !important',
          backgroundPosition: 'calc(100% - 0.1rem) center !important',
          appearance: 'none !important',
          // paddingRight: '0.7rem !important',
          backgroundImage: `url(${arrowLeft})`,
          backgroundRepeat: 'no-repeat',
          // opacity: 1,
        },
      },
      '& > li:last-child': {
        '& button': {
          color: '#286ce2 !important',
          backgroundPosition: 'calc(100% - 0.2rem) center !important',
          appearance: 'none !important',
          paddingRight: '0rem !important',
          backgroundImage: `url(${arrowRight})`,
          backgroundRepeat: 'no-repeat',
          // opacity: 1,
        },
      },
    },
    leftIconButton: {
      color: 'blue !important',
    },
    rightIconButton: {
      color: 'red !important',
    },
  },
}));

export default useStyles;
