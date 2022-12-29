import { createMuiTheme, ThemeProvider } from '@material-ui/core';
import AudioPlayer from 'material-ui-audio-player';
import useStyles from 'components/AudioPlayer/styles';
import { useEffect, useState } from 'react';

const muiTheme = createMuiTheme({});
// const src = 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3';
const AudioPlayerComponent = (props) => {
  // const classes = useStyles();
  // const { autoplay } = props;
  const [slider, setSlider] = useState(false);
  const [autoplay, setAutoplay] = useState(props.autoplay);
  const PlayAudio = () => {
    setSlider(true);
    setAutoplay(true);
  };
  return (
    <ThemeProvider theme={muiTheme}>
      <AudioPlayer
        elevation={0}
        width={slider ? 200 : 200}
        variation="primary"
        spacing={1}
        download={false}
        autoplay={true}
        // displaySlider={slider}
        order="standart"
        preload={true}
        loop={false}
        volume={false}
        src={props.path}
        time={'single'}
        timePosition={'end'}
        useStyles={useStyles}
        onPlayed={(event) => PlayAudio()}
      />
    </ThemeProvider>
  );
};
export default AudioPlayerComponent;
