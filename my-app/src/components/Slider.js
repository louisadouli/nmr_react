import * as React from 'react';
import Slider from '@mui/material/Slider';

// function valuetext(value) {
//   return `${value}°C`;
// }

const minDistance = 10;

export default function TimesweepSlider({value, setValue}) {

  const handleChange = (event, newValue, activeThumb) => {
    if (!Array.isArray(newValue)) {
      return;
    }

    if (activeThumb === 0) {
      setValue([Math.min(newValue[0], value[1] - minDistance), value[1]]);
    } else {
      setValue([value[0], Math.max(newValue[1], value[0] + minDistance)]);
    }
  };

  return (
    <div className="d-flex justify-content-center align-items-center" style={{maxHeight: '100%', height: '100%'}}>

      {/* <Slider
        getAriaLabel={()=>'Minimum distance'}
        value={value}
        onChange={handleChange}
        valueLabelDisplay="auto"
        getAriaValueText={value}
        disableSwap
        sx={{justifySelf: 'center', alignCenter:'center',  width: 250}}
        /> */}
    </div>
  );
}