import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => {
  return {
    root: {
      backgroundColor: 'inherit',
      transition: 'inherit',
      margin: '-15px 3px',
      [theme.breakpoints.down('sm')]: {
        width: '100%',
        backgroundColor: 'inherit',
        transition: 'inherit',
      },
    },
    icon: {
      fontSize: '20px',
    },
    loopIcon: {
      color: '#3f51b5',
      '&.selected': {
        color: '#0921a9',
      },
      '&:hover': {
        color: '#7986cb',
      },
      [theme.breakpoints.down('sm')]: {
        display: 'none',
      },
    },
    playIcon: {
      width: '40px',
      height: '40px',
      color: 'primary',
      '&:hover': {
        color: 'primary',
      },
    },
    pauseIcon: {
      width: '40px',
      height: '40px',
      color: 'primary',
      '&:hover': {
        color: 'primary',
      },
    },
    volumeIcon: {
      color: 'primary',
      background: 'primary',
    },
    volumeSlider: {
      color: 'black',
    },
    progressTime: {
      color: 'rgba(0, 0, 0, 0.54)',
    },
    mainSlider: {
      color: '#3f51b5',
      margin: '0px 10px',
      '& .MuiSlider-rail': {
        color: '#7986cb',
      },
      '& .MuiSlider-track': {
        color: '#3f51b5',
      },
      '& .MuiSlider-thumb': {
        color: '#303f9f',
      },
    },
  };
});

export default useStyles;
