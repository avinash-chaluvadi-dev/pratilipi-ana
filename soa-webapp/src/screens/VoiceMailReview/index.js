import React, { useEffect, useState } from 'react';
import { Grid, Divider, Typography, Button, Card } from '@material-ui/core';
import useStyles from './styles';
import RangeDP from 'components/RangeDP';
import ButtonsGroup from 'components/ButtonsGroup';
import DropDown from 'components/DropDown';
import CustomCard from 'screens/VoiceMailReview/Card';
import NotDataFound from 'screens/VoiceMailReview/noDataFound';
import ExcelIcon from 'static/images/excel.svg';
import SortIcon from 'static/images/sort.svg';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import Snackbar from '@mui/material/Snackbar';
import SnackbarContent from '@mui/material/SnackbarContent';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import { downloadBaseUrl } from 'api/config';
import Pagination from 'components/Pagination';
import { useSelector, useDispatch } from 'react-redux';
import moment from 'moment';
import {
  voiceMailReviewAction,
  voiceMailBox,
  reasonForCall,
  updateVoiceMail,
} from 'store/action/voiceMailReview';

const VoiceMailReview = (props) => {
  const classes = useStyles();
  const dispatch = useDispatch();
  const {
    voiceMailReviewResult,
    voiceMailReviewStatsResult,
    voiceMailBoxList,
    reasonForCallList,
    voiceMailUpdateRes,
  } = useSelector((state) => state.voiceMailReducer);
  const [selectedTab, setSelectedTab] = useState(1);
  const [anchorEl, setAnchorEl] = useState(null);
  const [startTime, setStartTime] = useState(null);
  const [selectedVoiceMailBox, setSelectedVoiceMailBox] = useState(null);
  const [endTime, setEndTime] = useState(null);
  const [btnValue, setBtnValue] = useState('Start Review');
  const [timesDropDownValues, setTimesDropDownValues] = useState([]);
  const [pageLimit] = useState(10);
  const [offset, setOffset] = useState(0);
  const [statsJson, setStatsJson] = useState([]);
  const [reasonForCallData, setReasonForCallData] = useState([]);
  const [isAutoPlay, setIsAutoPlay] = useState(false);
  const [voiceMailBoxData, setVoiceMailBoxData] = useState([]);
  const [startDate, setStartDate] = useState(
    moment(new Date()).format('YYYY-MM-DD')
  );
  const [endDate, setEndDate] = useState(moment(new Date()).format('YYYY-MM-DD'));
  const [commonFilter, setCommonFilter] = useState({
    date_start: startDate,
    date_end: endDate,
    limit: 10,
    offset: 0,
    state: 'Pending',
  });

  const open = Boolean(anchorEl);
  const [snackPack, setSnackPack] = useState([]);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [messageInfo, setMessageInfo] = useState(undefined);

  useEffect(() => {
    dispatch(voiceMailBox({ limit: 1000 }));
    dispatch(reasonForCall({ limit: 1000 }));
    setTimesDropDownValues(timeDropDownFun());
  }, [dispatch]);

  useEffect(() => {
    if (snackPack.length && !messageInfo) {
      setMessageInfo({ ...snackPack[0] });
      setSnackPack((prev) => prev.slice(1));
      setSnackbarOpen(true);
    } else if (snackPack.length && messageInfo && snackbarOpen) {
      setSnackbarOpen(false);
    }
  }, [snackPack, messageInfo, snackbarOpen]);

  const handleSnackbarClick = (message) => {
    setSnackPack((prev) => [...prev, { message, key: new Date().getTime() }]);
  };

  const handleSnackbarClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setSnackbarOpen(false);
  };

  const handleExited = () => {
    setMessageInfo(undefined);
  };

  const timeDropDownFun = () => {
    let arr = [];
    for (let i = 0; i < 25; i++) {
      arr.push({
        value: `${i}`.padStart(2, '0') + ':00',
        label: `${i}`.padStart(2, '0') + ':00',
      });
    }
    return arr;
  };

  const dropDownPrepare = (arr) => {
    return arr.map((item, idx) => {
      return {
        value: item.vmb_id,
        label: item.vmb_name,
      };
    });
  };

  const ReasonForCallDropDown = (arr) => {
    return arr.map((item, idx) => item.vmf_name);
  };

  useEffect(() => {
    setStatsJson(voiceMailReviewStatsResult);
    setVoiceMailBoxData(dropDownPrepare(voiceMailBoxList));
    setReasonForCallData(ReasonForCallDropDown(reasonForCallList));
  }, [
    voiceMailReviewResult,
    voiceMailReviewStatsResult,
    voiceMailBoxList,
    reasonForCallList,
  ]);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  const handMenu = (val, label) => {
    setOffset(0);
    setCommonFilter({ ...commonFilter, sort: val, label: label, offset: 0 });
    handleClose();
  };

  const onChangeTab = (val) => {
    setSelectedTab(val);
    setOffset(0);
    setIsAutoPlay(false);
    if (val === 4) {
      setBtnValue('Start Review');
      setCommonFilter({ ...commonFilter, state: 'Overdue', offset: 0 });
    } else if (val === 3) {
      setBtnValue('Edit Review');
      setCommonFilter({ ...commonFilter, state: 'Completed', offset: 0 });
    } else if (val === 2) {
      setBtnValue('Submit Review');
      setCommonFilter({ ...commonFilter, state: 'InProgress', offset: 0 });
    } else {
      setBtnValue('Start Review');
      setCommonFilter({ ...commonFilter, state: 'Pending', offset: 0 });
    }
  };

  const revState = (state) => {
    if (state === 'InProgress') return 'In Progress';
    else return state;
  };

  const buttonHandler = (reqBody, vm_id, vm_uuid) => {
    setIsAutoPlay(false);
    if (selectedTab === 2) {
      reqBody.vm_review_state = 'Completed';
      reqBody.vm_review_end_date = moment
        .tz(new Date(), 'America/New_York')
        .format();
    } else {
      reqBody.vm_review_state = 'InProgress';
      reqBody.vm_review_start_date = moment
        .tz(new Date(), 'America/New_York')
        .format();
    }
    dispatch(updateVoiceMail(reqBody, { voicemail_uuid: vm_uuid }));
  };

  useEffect(() => {
    if (Object.keys(voiceMailUpdateRes).length > 0) {
      // setIsAutoPlay(false);
      setOffset(0);
      if (selectedTab === 2) {
        setSelectedTab(3);
        setBtnValue('Edit Review');
        setCommonFilter({ ...commonFilter, state: 'Completed', offset: 0 });
      } else {
        setSelectedTab(2);
        setBtnValue('Submit Review');
        setCommonFilter({ ...commonFilter, state: 'InProgress', offset: 0 });
      }
    }
  }, [voiceMailUpdateRes]);

  useEffect(() => {
    // setIsAutoPlay(false);
    dispatch(voiceMailReviewAction(commonFilter));
  }, [dispatch, commonFilter]);

  useEffect(() => {
    if (voiceMailUpdateRes.vm_name && voiceMailUpdateRes.vm_review_state) {
      setIsAutoPlay(false);
      handleSnackbarClick(
        voiceMailUpdateRes.vm_name +
          ' moved to ' +
          revState(voiceMailUpdateRes.vm_review_state) +
          ' successfully.'
      );
    }
  }, [voiceMailUpdateRes]);

  const handleChangeStartTime = (val) => {
    setStartTime(val);
    setOffset(0);
    setCommonFilter({ ...commonFilter, time_start: val.value, offset: 0 });
  };

  const handleChangeToTime = (val) => {
    setEndTime(val);
    setOffset(0);
    setCommonFilter({ ...commonFilter, time_end: val.value, offset: 0 });
  };

  const handleChangeVoiceMail = (val) => {
    setSelectedVoiceMailBox(val);
    setOffset(0);
    setCommonFilter({ ...commonFilter, voicemail_box: val.value, offset: 0 });
  };

  const handleChangePagination = (event, value) => {
    let offsetVal = value === 1 ? 0 : (value - 1) * pageLimit;
    if (value < offset) {
      offsetVal = value === 1 ? 0 : value * pageLimit - pageLimit;
    }
    setOffset(offsetVal);
    setCommonFilter({ ...commonFilter, offset: offsetVal });
  };

  const handleDateChange = (data) => {
    setOffset(0);
    if (data.length === 2) {
      setStartDate(new Date(data[0]));
      setEndDate(new Date(data[1]));
      setCommonFilter({
        ...commonFilter,
        date_start: moment(new Date(data[0])).format('YYYY-MM-DD'),
        date_end: moment(new Date(data[1])).format('YYYY-MM-DD'),
        offset: 0,
      });
    } else {
      setStartDate(new Date(data[0]));
      setEndDate(new Date(data[0]));
      setCommonFilter({
        ...commonFilter,
        date_start: moment(new Date(data[0])).format('YYYY-MM-DD'),
        date_end: moment(new Date(data[0])).format('YYYY-MM-DD'),
        offset: 0,
      });
    }
  };
  const loadeFunStart = () => {
    dispatch({
      type: 'START_LOADER',
      payload: { isLoader: true },
    });
  };
  const loadeFunStop = () => {
    dispatch({
      type: 'STOP_LOADER',
      payload: { isLoader: false },
    });
  };
  const excelDownloadReport = () => {
    loadeFunStart();
    let accessToken = sessionStorage.getItem('accessToken');
    let url = '';
    url += `download_excel=true`;
    for (let obj in commonFilter) {
      url += `&${obj}=${commonFilter[obj]}`;
    }
    url = `${downloadBaseUrl}/list-voicemails?${url}`;
    const filename = 'voiceMailReport.xlsx';
    let xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'blob';
    xhr.setRequestHeader('Authorization', 'Bearer ' + accessToken);
    xhr.onload = function (e) {
      if (this.status === 200) {
        const blob = this.response;
        const a = document.createElement('a');
        document.body.appendChild(a);
        const blobUrl = window.URL.createObjectURL(blob);
        a.href = blobUrl;
        a.download = filename;
        a.click();
        setTimeout(() => {
          window.URL.revokeObjectURL(blobUrl);
          document.body.removeChild(a);
        }, 0);
      }
      loadeFunStop();
    };
    xhr.send();
  };

  const getCount = () => {
    if (selectedTab === 4) {
      return statsJson.overdue_count;
    } else if (selectedTab === 3) {
      return statsJson.completed_count;
    } else if (selectedTab === 2) {
      return statsJson.in_progress_count;
    } else {
      return statsJson.pending_count;
    }
  };

  const claerFilter = async () => {
    await setEndDate('');
    await setStartDate('');
    await setStartTime(null);
    await setEndTime(null);
    await setSelectedVoiceMailBox(null);
    await setCommonFilter({
      limit: 10,
      offset: 0,
      state: commonFilter.state,
    });
  };

  return (
    <Card className={classes.Card}>
      <Grid
        xs={12}
        className={classes.lsfInnerSubCard}
        item
        style={{ padding: '2px 40px 20px 0' }}
      >
        <Typography className={classes.textLeft}>Voicemail(s) Review</Typography>
        <Button
          color="secondary"
          onClick={() => claerFilter()}
          variant="outlined"
          value="ClearFilter"
        >
          Clear Filter
        </Button>
      </Grid>
      <Grid xs={12} item className={classes.lsfInnerSubCard}>
        <Grid xs={3} item style={{ padding: '2px 10px 10px 5px' }}>
          <Typography
            className={classes.textLeftFontSize}
            style={{ paddingLeft: '0px' }}
          >
            Select Date
          </Typography>
          <RangeDP
            handleDateChange={handleDateChange}
            startDate={startDate}
            endDate={endDate}
          />
        </Grid>
        <Grid xs={2} item style={{ padding: '2px 10px 10px 0 ' }}>
          <Typography className={classes.textLeftFontSize}>
            Select Time(From)
          </Typography>

          <DropDown
            listUserData={timesDropDownValues}
            handleChangeDropDown={handleChangeStartTime}
            selectedVal={startTime}
          />
        </Grid>
        <Grid xs={2} item style={{ padding: '2px 10px 10px 0 ' }}>
          <Typography className={classes.textLeftFontSize}>
            Select Time(To)
          </Typography>
          <DropDown
            listUserData={timesDropDownValues}
            handleChangeDropDown={handleChangeToTime}
            selectedVal={endTime}
          />
        </Grid>
        <Grid xs={3} item style={{ padding: '2px 10px 10px 0 ' }}>
          <Typography className={classes.textLeftFontSize}>Voicemail Box</Typography>

          <DropDown
            listUserData={voiceMailBoxData}
            handleChangeDropDown={handleChangeVoiceMail}
            placeHolderText="Select Voicemail Box"
            selectedVal={selectedVoiceMailBox}
          />
        </Grid>
        <Grid
          xs={5}
          item
          style={{
            padding: '2px 0px 10px 5px ',
            border: '1px dashed #286ce2',
            background: '#f0f5ff',
            marginRight: '40px',
            lineHeight: '30px',
          }}
        >
          <Grid xs={12} item className={classes.innerSubCard}>
            <Grid xs={4} item className={classes.innerSubCard}>
              <Grid xs={8} item className={classes.innerSubCardRed}>
                Overdue
              </Grid>
              <Grid xs={1} item className={classes.innerSubCardRed}>
                :
              </Grid>
              <Grid xs={3} item className={classes.innerSubCardRed}>
                {statsJson.overdue_count || 0}
              </Grid>
            </Grid>
            <Divider className={classes.divider} orientation="vertical" />
            <Grid xs={4} item className={classes.innerSubCard}>
              <Grid xs={8} item className={classes.innerSubCard}>
                Pending
              </Grid>
              <Grid xs={1} item className={classes.innerSubCard}>
                :
              </Grid>
              <Grid xs={3} item className={classes.innerSubCardBold}>
                {statsJson.pending_count || 0}
              </Grid>
            </Grid>
            <Divider className={classes.divider} orientation="vertical" />
            <Grid xs={4} item className={classes.innerSubCard}>
              <Grid xs={8} item className={classes.innerSubCard}>
                In Progress
              </Grid>
              <Grid xs={1} item className={classes.innerSubCard}>
                :
              </Grid>
              <Grid xs={3} item className={classes.innerSubCardBold}>
                {statsJson.in_progress_count || 0}
              </Grid>
            </Grid>
          </Grid>
          <Grid xs={12} item className={classes.innerSubCard}>
            <Grid xs={4} item className={classes.innerSubCard}>
              <Grid xs={8} item className={classes.innerSubCard}>
                Completed
              </Grid>
              <Grid xs={1} item className={classes.innerSubCard}>
                :
              </Grid>
              <Grid xs={3} item className={classes.innerSubCardBold}>
                {statsJson.completed_count || 0}
              </Grid>
            </Grid>
            <Divider className={classes.divider} orientation="vertical" />
            <Grid xs={4} item className={classes.innerSubCard}>
              <Grid xs={8} item className={classes.innerSubCard}>
                Total
              </Grid>
              <Grid xs={1} item className={classes.innerSubCard}>
                :
              </Grid>
              <Grid xs={3} item className={classes.innerSubCardBold}>
                {statsJson.total_count || 0}
              </Grid>
            </Grid>
            <Divider className={classes.dividerInvisible} orientation="vertical" />
            <Grid xs={4} item className={classes.innerSubCard}>
              {' '}
            </Grid>
          </Grid>
        </Grid>
      </Grid>

      <Grid
        xs={12}
        item
        className={classes.lsfInnerSubCard}
        style={{ margin: '20px 0px 20px 4px' }}
      >
        <Grid
          item
          xs={5}
          className={` ${classes.sideCard}`}
          // style={{ marginLeft: 10 }}
        >
          <ButtonsGroup
            items={[
              `Pending (${statsJson.pending_count || 0})`,
              `In Progress (${statsJson.in_progress_count || 0})`,
              `Completed (${statsJson.completed_count || 0})`,
              `Overdue (${statsJson.overdue_count || 0})`,
            ]}
            selectedBtn={selectedTab}
            bold={'bold'}
            onClickDateTab={onChangeTab}
          />
        </Grid>
        <Grid
          item
          xs={5}
          className={`${classes.textAlignRight} ${classes.lsfInnerSubCardBox}`}
          style={{ paddingRight: 40 }}
        >
          <Typography className={classes.sortBorderCls}>
            <Button
              id="basic-button"
              aria-controls={open ? 'basic-menu' : undefined}
              aria-haspopup="true"
              aria-expanded={open ? 'true' : undefined}
              onClick={handleClick}
              varient="primary"
              color="primary"
              style={{
                textTransform: 'none',
                fontWeight: 'bold',
                fontSize: 16,
                fontFamily: 'Lato',
              }}
              startIcon={
                <img
                  src={SortIcon}
                  alt=""
                  style={{ margin: '0px 5px' }}
                  onClick={{}}
                />
              }
            >
              {commonFilter?.label ? `Sort By ${commonFilter?.label}` : 'Sort'}
            </Button>
            <Menu
              id="basic-menu"
              anchorEl={anchorEl}
              open={open}
              onClose={handleClose}
              MenuListProps={{
                'aria-labelledby': 'basic-button',
              }}
            >
              <MenuItem onClick={() => handMenu('receivedtime', 'Time')}>
                Sort By Time
              </MenuItem>
              <MenuItem onClick={() => handMenu('membername', 'Member Name')}>
                Sort By Member Name
              </MenuItem>
              <MenuItem onClick={() => handMenu('reasoncall', 'Reason for Call')}>
                Sort By Reason For Call
              </MenuItem>
              <MenuItem onClick={() => handMenu('callnumber', 'Call Back Number')}>
                Sort By Call Back Number
              </MenuItem>
            </Menu>
          </Typography>
          <Typography
            onClick={excelDownloadReport}
            className={`${classes.borderCls} ${classes.lsfInnerSubCardBox}`}
            style={{
              textTransform: 'none',
              fontWeight: 'bold',
              fontSize: 16,
              cursor: 'pointer',
            }}
          >
            <img src={ExcelIcon} alt="" style={{ margin: '0px 10px -6px 10px' }} />
            Download Excel Report
          </Typography>
          {/* </a> */}
        </Grid>
      </Grid>

      {voiceMailReviewResult.length === 0 ? (
        <NotDataFound selectedtab={selectedTab} />
      ) : (
        voiceMailReviewResult.map((item) => (
          <CustomCard
            itemValue={item}
            selectedTab={selectedTab}
            buttonHandler={buttonHandler}
            btnValue={btnValue}
            reasonForCallData={reasonForCallData}
            key={item.vm_uuid}
            autoPlay={isAutoPlay}
          />
        ))
      )}
      <Grid xs={12} item style={{ paddingLeft: '45%', paddingTop: '1%' }}>
        {voiceMailReviewResult.length > 0 && (
          <Pagination
            limit={pageLimit}
            page={offset === 0 ? 1 : offset / pageLimit + 1}
            handleChangePagination={handleChangePagination}
            totalrecords={Math.ceil(getCount() / pageLimit)}
          />
        )}
      </Grid>
      <Snackbar
        transformOrigin={{ vertical: 'bottom', horizontal: 'left' }}
        autoHideDuration={6000}
        key={messageInfo ? messageInfo.key : undefined}
        open={snackbarOpen}
        onClose={handleSnackbarClose}
        TransitionProps={{ onExited: handleExited }}
        className={classes.snackbar}
      >
        <SnackbarContent
          style={{
            backgroundColor: 'white',
            color: '#333333',
            width: '0px',
            borderLeft: '5px solid #d20a3c',
            fontWeight: 'bold',
            fontFamily: 'Lato',
            fontSize: '14px',
          }}
          action={
            <React.Fragment>
              <IconButton
                aria-label="close"
                color="inherit"
                sx={{ marginRight: '-15px', marginTop: '-90px' }}
                onClick={handleSnackbarClose}
              >
                <CloseIcon />
              </IconButton>
            </React.Fragment>
          }
          message={messageInfo ? messageInfo.message : undefined}
        />
      </Snackbar>
    </Card>
  );
};
export default VoiceMailReview;
