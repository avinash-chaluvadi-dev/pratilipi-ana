import React, { useEffect, useState } from 'react';
import { Grid, Typography, Button, Card, Paper, TextField } from '@material-ui/core';
import useStyles from './styles';
import MultiSelect from 'components/MultiSelect';
import AudioComponent from 'components/AudioPlayer';
import PlayIcon from 'static/images/play.svg';
import { styled } from '@mui/material/styles';
import Tooltip, { tooltipClasses } from '@mui/material/Tooltip';
import MyTimer from 'components/Timer';
import moment from 'moment-timezone';
import Checkbox from '@material-ui/core/Checkbox';
import { ConstantValue } from 'utils/constant';

const LightTooltip = styled(({ className, ...props }) => (
  <Tooltip {...props} classes={{ popper: className }} />
))(({ theme }) => ({
  [`& .${tooltipClasses.tooltip}`]: {
    backgroundColor: theme.palette.common.white,
    color: 'rgba(0, 0, 0, 0.87)',
    boxShadow: theme.shadows[1],
    fontSize: 11,
    width: '50%',
    marginLeft: 50,
    fontWeight: 'bold',
  },
}));

const CustomCard = (props) => {
  const classes = useStyles();
  const maxReviewerCharCount = ConstantValue.MAX_REVIEWER_CHAR_COUNT;
  let {
    itemValue,
    selectedTab,
    buttonHandler,
    btnValue,
    reasonForCallData,
    autoPlay,
  } = props;

  const [pendingBtn, setPendingBtn] = useState(false);
  const [mailBody, setMailBody] = useState('');
  const [reviewerComments, setReviewerComments] = useState('');
  const [extensionId, setExtensionId] = useState('');
  const [memberName, setMemberName] = useState('');
  const [callbackNumber, setCallbackNumber] = useState('');
  const [callForReason, setCallForReason] = useState('');
  const [memberCalledBack, setMemberCalledBack] = useState(false);
  const [callBackNumberReachable, setCallBackNumberReachable] = useState(false);
  const [expiryTimestamp, setExpiryTimestamp] = useState(
    new Date(itemValue.vm_timestamp)
  );
  const [autoPlayOnOff, setAutoPlayOnOff] = useState(autoPlay);
  const [is24HrsExceed, setIs24HrsExceed] = useState(false);
  const [vmbName, setVmbName] = useState('');

  useEffect(() => {
    setMailBody(itemValue.vm_transcript_dtls || '');
    setVmbName(itemValue.vmb_name || '');
    setReviewerComments(itemValue.vm_reviewer_comments || '');
    setExtensionId(itemValue.vm_extension_id || '');
    setMemberName(itemValue.vm_member_name || '');
    setCallbackNumber(itemValue.vm_callback_no || '');
    setCallForReason(itemValue.vm_call_reason.reason || '');
    setMemberCalledBack(itemValue.vm_member_called_back || false);
    setCallBackNumberReachable(itemValue.vm_callback_no_reachable || false);
    setExpiryTimestamp(new Date(itemValue.vm_timestamp));
    expiryTimestamp.setDate(expiryTimestamp.getDate() + 1);
    expiryTimestamp.setMinutes(
      expiryTimestamp.getMinutes() - expiryTimestamp.getTimezoneOffset() + 240
    );
  }, [itemValue]);

  useEffect(() => {
    setAutoPlayOnOff(autoPlay);
  }, [autoPlay]);

  const onChangeMailText = (e) => {
    setMailBody(e.target.value);
  };

  const onChangeReviewerComments = (e) => {
    setReviewerComments(e.target.value);
  };

  const handleMemberName = (e) => {
    setMemberName(e.target.value);
  };

  const handleCallbackNumber = (e) => {
    setCallbackNumber(e.target.value);
  };

  const onChangeExtensionVal = (e) => {
    setExtensionId(e.target.value);
  };

  const onChangeMemberCalledBack = (e) => {
    setMemberCalledBack(e.target.checked);
  };

  const onChangeCallBackNumberReachable = (e) => {
    setCallBackNumberReachable(e.target.checked);
  };

  const pendingBtnHandler = () => {
    setPendingBtn(true);
  };

  const playBtnHandler = () => {
    setPendingBtn(true);
  };

  const patchApi = () => {
    let reqBody = {
      vm_uuid: itemValue.vm_uuid,
      vm_system_state: itemValue.vm_system_state,
      vm_review_state: itemValue.vm_review_state,
      vm_member_name: memberName || itemValue.vm_member_name,
      vm_active_status: true,
      vm_timestamp: itemValue.vm_timestamp,
      vm_ner: itemValue.vm_ner,
      vm_call_reason: { reason: callForReason },
      vm_callback_no: callbackNumber,
      vm_extension_id: extensionId,
      vm_transcript_dtls: mailBody,
      vm_normalized_dtls: mailBody,
      vm_reviewer_name: sessionStorage.getItem('userName'),
      vm_review_start_date: itemValue.vm_review_start_date,
      vm_review_end_date: itemValue.vm_review_end_date,
      vm_reviewer_comments: reviewerComments,
      vm_member_called_back: memberCalledBack,
      vm_callback_no_reachable: callBackNumberReachable,
    };
    buttonHandler(reqBody, itemValue.vm_id, itemValue.vm_uuid);
  };

  const handleMDChange = (value) => {
    setCallForReason(value);
  };

  useEffect(() => {
    let startDate = moment.tz(itemValue?.vm_timestamp, 'America/New_York');
    let endDate =
      selectedTab === 2
        ? moment.tz(itemValue?.vm_review_start_date, 'America/New_York')
        : moment.tz(itemValue?.vm_review_end_date, 'America/New_York');
    if (startDate && endDate) {
      let diff = Math.abs(startDate - endDate) / 3600000;
      if (diff > 24) {
        setIs24HrsExceed(Math.round(diff));
      }
    }
  });

  return (
    <Card className={classes.Card1}>
      <Grid
        xs={12}
        item
        style={{ padding: '0px 0px 15px 20px' }}
        className={classes.lsfInnerSubCard}
      >
        <Grid xs={6} item className={classes.lsfInnerSubCardBox}>
          <Typography className={classes.textLeft}>{itemValue.vm_name}</Typography>
          <Typography className={classes.textLeftPadding}>
            received on{' '}
            <b>
              {moment
                .tz(itemValue.vm_timestamp, 'America/New_York')
                .format('MM-DD-YYYY   ||   HH:mm')}{' '}
              <span style={{ color: '#286ce2' }}>(ET)</span>
            </b>
          </Typography>
          {(selectedTab !== 3 || (selectedTab === 3 && itemValue.vm_is_overdue)) && (
            <LightTooltip
              title="Remaining Time To Review Voice Mail"
              arrow
              placement="top"
            >
              <MyTimer expiryTimestamp={expiryTimestamp} />
            </LightTooltip>
          )}
        </Grid>
        <Grid
          xs={6}
          item
          className={`${classes.lsfInnerSubCardBox} ${classes.flexEnd}`}
        >
          <Grid
            xs={6}
            item
            style={{ marginLeft: 10 }}
            className={`${classes.divBoxRound} ${classes.lsfInnerSubCardBox} ${
              selectedTab !== 2 ? classes.disableCls : {}
            } ${
              (selectedTab === 2 || selectedTab === 3) &&
              sessionStorage.getItem('userName') !== itemValue.vm_reviewer_name
                ? classes.disableCls
                : {}
            }`}
          >
            <Typography className={classes.extensionCls}>Extension ID :</Typography>
            <input
              type="text"
              value={extensionId}
              onChange={onChangeExtensionVal}
              className={classes.inputWithoutBorder}
            />
          </Grid>
          <Grid
            xs={pendingBtn ? 4 : 2}
            item
            className={`${classes.lsfInnerSubCardBox} ${classes.flexEnd}`}
          >
            {itemValue.vm_audio_url !== '' &&
              itemValue.vm_call_duration !== '' &&
              !pendingBtn && (
                <Typography
                  className={`${classes.paddingLeftCls} ${
                    selectedTab !== 2 ? classes.disableCls : {}
                  } ${
                    (selectedTab === 2 || selectedTab === 3) &&
                    sessionStorage.getItem('userName') !== itemValue.vm_reviewer_name
                      ? classes.disableCls
                      : {}
                  }`}
                >
                  {itemValue.vm_call_duration}
                </Typography>
              )}
            <Paper style={{ boxShadow: 'none' }}>
              {itemValue.vm_audio_url !== '' && !pendingBtn && (
                <Typography
                  onClick={pendingBtnHandler}
                  className={`${selectedTab !== 2 ? classes.disableCls : {}} ${
                    (selectedTab === 2 || selectedTab === 3) &&
                    sessionStorage.getItem('userName') !== itemValue.vm_reviewer_name
                      ? classes.disableCls
                      : {}
                  }`}
                >
                  <img src={PlayIcon} alt="" />
                </Typography>
              )}
              {itemValue.vm_audio_url !== '' && pendingBtn && (
                <Typography>
                  <AudioComponent
                    path={itemValue.vm_audio_url}
                    autoplay={autoPlayOnOff}
                    selectedTab={selectedTab}
                  />
                </Typography>
              )}
            </Paper>
          </Grid>
          <Grid xs={4} item>
            <Button
              color="primary"
              size="small"
              variant="contained"
              style={{
                textTransform: 'none',
                borderRadius: 8,
                fontSize: 16,
                padding: '2px 20px',
                minWidth: '150px',
              }}
              className={`${
                (selectedTab === 2 || selectedTab === 3) &&
                sessionStorage.getItem('userName') !== itemValue.vm_reviewer_name
                  ? classes.disableCls
                  : {}
              }`}
              onClick={patchApi}
            >
              {btnValue}
            </Button>
          </Grid>
        </Grid>
      </Grid>
      <Grid
        item
        xs={12}
        className={`${classes.subCard} ${
          selectedTab !== 2 ? classes.disableCls : {}
        } ${
          (selectedTab === 2 || selectedTab === 3) &&
          sessionStorage.getItem('userName') !== itemValue.vm_reviewer_name
            ? classes.disableCls
            : {}
        }`}
      >
        <Grid item xs={9}>
          <Typography className={classes.subTextLeft}>Member Messages</Typography>
          <textarea
            type="text"
            multiline
            rows="30"
            className={classes.TextboxCopy}
            value={mailBody}
            onChange={onChangeMailText}
          />
        </Grid>
        <Grid item xs={3} className={classes.reviewerCommentsContainer}>
          <Typography className={classes.subTextRight}>Reviewer Comments</Typography>
          <textarea
            type="text"
            multiline
            rows="30"
            className={classes.TextboxCopy}
            placeholder="No comments added yet"
            value={reviewerComments}
            onChange={onChangeReviewerComments}
            maxLength={maxReviewerCharCount}
          />
          {reviewerComments.length > 0 && (
            <span className={classes.characterCount}>
              {maxReviewerCharCount - reviewerComments.length} characters left
            </span>
          )}
        </Grid>
      </Grid>
      <Grid
        xs={12}
        item
        className={classes.lsfInnerSubCard}
        style={{ margin: '10px 25px' }}
      >
        {' '}
        <Grid
          xs={8}
          item
          className={`${classes.lsfInnerSubCard} ${
            selectedTab !== 2 ? classes.disableCls : {}
          } ${
            (selectedTab === 2 || selectedTab === 3) &&
            sessionStorage.getItem('userName') !== itemValue.vm_reviewer_name
              ? classes.disableCls
              : {}
          }`}
        >
          <Grid xs={4} item style={{ padding: '0px 30px 10px 0 ' }}>
            <Typography className={classes.textLeftFontSize}>Member Name</Typography>
            <TextField
              variant="outlined"
              className={classes.Textbox}
              value={memberName}
              onChange={handleMemberName}
            />
          </Grid>
          <Grid xs={4} item style={{ padding: '0px 30px 10px 0 ' }}>
            <Typography className={classes.textLeftFontSize}>
              Call Back Number
            </Typography>
            <TextField
              variant="outlined"
              className={classes.Textbox}
              value={callbackNumber}
              onChange={handleCallbackNumber}
            />
          </Grid>
          <Grid xs={4} item style={{ padding: '0px 45px 0px 0 ' }}>
            <Typography className={classes.textLeftFontSize}>
              Reason For Call
            </Typography>
            <MultiSelect
              options={reasonForCallData}
              selectedVal={
                callForReason && callForReason.length > 0 ? callForReason : []
              }
              handleMDChange={handleMDChange}
            />
          </Grid>
        </Grid>
        <Grid
          xs={4}
          item
          style={{ padding: '0px 0px 0px 90px ' }}
          className={` ${selectedTab !== 2 ? classes.disableCls : {}} ${
            (selectedTab === 2 || selectedTab === 3) &&
            sessionStorage.getItem('userName') !== itemValue.vm_reviewer_name
              ? classes.disableCls
              : {}
          }`}
        >
          <Typography className={classes.textLeftFontSize}>
            <Checkbox
              checked={memberCalledBack}
              onChange={onChangeMemberCalledBack}
              style={{
                color: '#286ce2',
              }}
              size="small"
            />
            Member Already Called Back
          </Typography>
          <Typography className={classes.textLeftFontSize}>
            <Checkbox
              checked={callBackNumberReachable}
              onChange={onChangeCallBackNumberReachable}
              style={{
                color: '#286ce2',
              }}
              size="small"
            />
            Reachable at Callback Number
          </Typography>
        </Grid>
      </Grid>
      <Grid item xs={12} className={classes.lsfInnerSubCard}>
        <Grid
          xs={2}
          item
          style={{
            textAlign: 'left',
            padding: '0 0 5px 27px',
            color: '#286ce2',
            fontWeight: 'bold!important',
          }}
        >
          {' '}
          <Typography component="span" style={{ fontWeight: 'bold!important' }}>
            {vmbName || itemValue?.vmb_name || 'No Mail Box Is Assigned'}
          </Typography>
        </Grid>
        {selectedTab !== 1 && selectedTab !== 4 && (
          <Grid className={classes.textAlignRight} style={{ marginBottom: 10 }}>
            <Typography component="span" class="Review-submitted-by">
              * {selectedTab === 2 ? 'In Progress ' : 'Review submitted '} by{' '}
              <Typography component="span" class="text-style-1">
                {' '}
                {itemValue.vm_reviewer_name}
              </Typography>{' '}
              on{' '}
              {selectedTab === 2 ? (
                <>
                  <b>
                    {' '}
                    {moment
                      .tz(itemValue.vm_review_start_date, 'America/New_York')
                      .format('MM-DD-YYYY   ||   HH:mm')}
                  </b>
                  <span style={{ color: '#286ce2' }}>(ET)</span>
                </>
              ) : (
                <>
                  <b>
                    {moment
                      .tz(itemValue.vm_review_end_date, 'America/New_York')
                      .format('MM-DD-YYYY   ||   HH:mm')}
                  </b>
                  <span style={{ color: '#286ce2' }}>(ET)</span>
                </>
              )}
              {}
            </Typography>
          </Grid>
        )}
      </Grid>
    </Card>
  );
};
export default CustomCard;
