import React from 'react'
const dict = {
    "welcome" : "20",
    "setup" : "40",
    "setupgpc": "40",
    "timesweep" : "60",
    "conversion" : "80",
    "init" : "100",
}
const ProgressBar = ({page}) => {
  return (
    <div className="progress">
        <div className="progress-bar" role="progressbar" style={{width: `${dict[page]}%`}} aria-valuenow={dict[page]} aria-valuemin="0" aria-valuemax="100">{dict[page]}%</div>
    </div>
  )
}

export default ProgressBar