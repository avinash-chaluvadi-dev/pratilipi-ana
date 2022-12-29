import { Box, ButtonGroup, Button } from '@material-ui/core';

const ButtonGroupComponent = (props) => {
  let { items, bold, transformvalue, selectedBtn } = props;
  return (
    <Box
      display="block"
      component="div"
      justifyContent="space-between"
      mr={1}
      p={1}
      style={{ paddingLeft: '2px' }}
    >
      <ButtonGroup
        aria-label="outlined primary button group"
        disableElevation
        variant="contained"
        style={{
          boxShadow:
            '0px 3px 1px -2px rgb(0 0 0 / 20%), 0px 2px 2px 0px rgb(0 0 0 / 14%), 0px 1px 5px 0px rgb(0 0 0 / 12%)',
          height: 40,
          borderRadius: '8px',
          width: '155%',
        }}
      >
        {items.map((item, idx) => (
          <Button
            className={`${bold} ${transformvalue} ${'selectDateBox' + idx}`}
            style={
              selectedBtn === idx + 1
                ? {
                    background: '#286ce2',
                    color: '#fff',
                    margin: '-1px',
                    padding: '9px 24px',
                    backgroundColor: '#286ce2',
                    fontFamily: 'Lato',
                    fontSize: 16,
                    fontWeight: 'bold',
                    textTransform: 'none',
                    width: '50%',
                  }
                : {
                    background: 'white',
                    padding: '9px 24px',
                    fontFamily: 'Lato',
                    fontSize: 16,
                    fontWeight: 'bold',
                    textTransform: 'none',
                    color: '#286ce2',
                    width: '50%',
                  }
            }
            onClick={() => props.onClickDateTab(idx + 1)}
          >
            {item}
          </Button>
        ))}
      </ButtonGroup>
    </Box>
  );
};

export default ButtonGroupComponent;
