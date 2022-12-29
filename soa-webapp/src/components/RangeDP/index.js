import React, { useState, useRef, useEffect } from 'react';
import DatePicker from 'react-multi-date-picker';
import Box from '@mui/material/Box';
import { Button } from '@material-ui/core';
import RangeDPStyles from 'components/RangeDP/styles';
import ArrowForwardSharpIcon from '@mui/icons-material/ArrowForwardSharp';
import ArrowBackSharpIcon from '@mui/icons-material/ArrowBackSharp';
import CalenderIcon from 'static/images/calenderIcon.svg';
import { TextField, IconButton } from '@material-ui/core';

const RangeDP = (props) => {
  let { inputWidth, handleDateChange, startDate, endDate } = props;
  const [val, setVal] = useState(new Date());
  const [oldval, setOldVal] = useState(new Date());
  const ref = useRef();
  const [shouldCloseCalendar, setShouldCloseCalendar] = useState(false);
  const weekDays = ['SU', 'M', 'TU', 'W', 'TH', 'F', 'SA'];
  const months = [
    'JANUARY',
    'FEBRUARY',
    'MARCH',
    'APRIL',
    'MAY',
    'JUNE',
    'JULY',
    'AUGUST',
    'SEPTEMBER',
    'OCTOBER',
    'NOVEMBER',
    'DECEMBER',
  ];
  const handleValChange = (data) => {
    setVal(data);
  };

  useEffect(() => {
    if (endDate === '' && startDate === '') {
      setVal('');
    }
  }, [startDate, endDate]);

  const MyPlugin = ({ position }) => {
    return (
      <div>
        <Box sx={{ width: '100%', typography: 'body1' }}></Box>
      </div>
    );
  };

  const BottomPlugin = ({ onClose }) => {
    const classes = RangeDPStyles();
    return (
      <div style={{ textAlign: 'right' }}>
        <Button
          variant="outlined"
          color="primary"
          className={classes.applyBtnCls}
          onClick={() => {
            setVal(oldval);
            setShouldCloseCalendar(true);
            setTimeout(() => {
              ref.current.closeCalendar();
            }, 20);
          }}
        >
          Cancel
        </Button>
        <Button
          variant="contained"
          color="primary"
          className={classes.applyBtnCls}
          onClick={() => {
            setOldVal(val);
            handleDateChange(val);
            setShouldCloseCalendar(true);
            setTimeout(() => {
              ref.current.closeCalendar();
            }, 20);
          }}
        >
          Apply
        </Button>
      </div>
    );
  };

  const CustomButton = ({ direction, handleClick, disabled }) => {
    return (
      <i
        onClick={handleClick}
        style={{
          padding: '0 10px',
          fontWeight: 'bold',
          color: disabled ? 'gray' : '#286ce2',
          fontSize: '20px',
        }}
        className={disabled ? 'cursor-default' : 'cursor-pointer'}
      >
        {direction === 'right' ? <ArrowForwardSharpIcon /> : <ArrowBackSharpIcon />}
      </i>
    );
  };

  const CustomInput = ({ openCalendar, value }) => {
    const classes = RangeDPStyles();
    return (
      <TextField
        onFocus={openCalendar}
        value={value}
        className={classes.inputBoxCls}
        id="standard-bare"
        variant="outlined"
        placeholder="Select Date"
        InputProps={{
          endAdornment: (
            <IconButton onClick={openCalendar}>
              <img
                src={CalenderIcon}
                alt=""
                width={inputWidth ? inputWidth : 16}
                height={15}
                onClick={openCalendar}
              />
            </IconButton>
          ),
        }}
      />
    );
  };

  return (
    <>
      <DatePicker
        render={<CustomInput />}
        range={true}
        weekDays={weekDays}
        months={months}
        value={val}
        ref={ref}
        multiple={false}
        onChange={(dateValue) => handleValChange(dateValue)}
        format={'MM-DD-YYYY'}
        inputClass="red"
        numberOfMonths={2}
        renderButton={<CustomButton />}
        plugins={[<MyPlugin position="top" />, <BottomPlugin position="bottom" />]}
        // calendarPosition="top-right"
        arrow={false}
        onOpenPickNewDate={false}
        onOpen={() => setShouldCloseCalendar(false)}
        onClose={() => shouldCloseCalendar}
      />
    </>
  );
};

export default RangeDP;
