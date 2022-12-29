import React, { useState, useEffect } from 'react';
import Checkbox from '@material-ui/core/Checkbox';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import { MenuProps, useStyles } from './util';
import selectIcon from 'static/images/selectIcon.png';

function MultiSelect(props) {
  let { options, selectedVal, handleMDChange } = props;
  const classes = useStyles();
  const [selected, setSelected] = useState([]);
  useEffect(() => {
    setSelected(selectedVal);
  }, [selectedVal]);

  const handleChange = (event) => {
    const value = event.target.value;
    setSelected(value);
    handleMDChange(value);
  };

  return (
    <FormControl className={classes.formControl}>
      <Select
        IconComponent={() => (
          <img
            src={selectIcon}
            alt=""
            width={'20px'}
            height={'20px'}
            className={classes.selectDropdown}
          />
        )}
        disableUnderline
        labelId="mutiple-select-label"
        renderValue={() => {
          if (!selected) return 'Select Values';
          if (selected.length > 1) return selected.join(', ');
          else return selected;
        }}
        multiple
        value={selected}
        onChange={handleChange}
        MenuProps={MenuProps}
      >
        {options.map((option) => (
          <MenuItem key={option} value={option}>
            <ListItemIcon>
              <Checkbox
                checked={selected.indexOf(option) > -1}
                style={{
                  color: '#286ce2',
                }}
              />
            </ListItemIcon>
            <ListItemText primary={option} />
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}

export default MultiSelect;
