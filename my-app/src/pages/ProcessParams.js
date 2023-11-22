import React from 'react'
import axios from 'axios'

const ProcessParams = ({page, setPage}) => {
  const run=()=>{
    axios.get('http://localhost:5000//outputCSV-params')
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });

  }
  return (
    <>
      <h1 className='mb-3'>Process with 3-4 pumps</h1>
      <div>
        <button className="btn btn-danger mb-5" onClick={()=>setPage('uploadCSV')}>Previous Page</button>
      </div>

      <div>
        <button onClick={run}>Run Pumps</button>
      </div>
    </>
  )
}

export default ProcessParams