import React from 'react';
import { useTimer } from 'react-timer-hook';

export default function MyTimer({ expiryTimestamp }) {
  const { seconds, minutes, hours } = useTimer({
    expiryTimestamp,
    onExpire: () => console.warn(''),
  });
  const formatTime = (time) => {
    return String(time).padStart(2, '0');
  };

  return (
    <div
      style={{
        width: '70px',
        height: 20,
        padding: '4px 13px',
        borderRadius: 32,
        border: 'solid 1px #ff2236',
        color: '#ff2236',
        fontSize: 16,
      }}
    >
      {hours > 0 || minutes > 0 || seconds > 0 ? (
        <div style={{ fontSize: '16px', color: 'red' }}>
          <span>{formatTime(hours)}</span>:<span>{formatTime(minutes)}</span>:
          <span>{formatTime(seconds)}</span>
        </div>
      ) : (
        <div style={{ fontSize: '16px', color: 'red' }}>
          <span>Overdue</span>
        </div>
      )}
    </div>
  );
}
