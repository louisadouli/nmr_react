import React, {useState} from 'react'
import axios from 'axios'
const ConversionPage = ({page, setPage}) => {
const [value, setValue] = useState('1')
// const [error, setError]=useState('')
const handleSubmit = () =>{
  if(parseFloat(value)){
  axios.get(`http://localhost:5000/conversion?c=${value}`)
  .then(response => {
    console.log(response.data);
  })
  .catch(error => {
    console.log(error);
  });
    setPage('experimentParams')
  }
  else{
    console.log('error')
  }
}
  return (
    <>
    <h1 className='mb-5'>
      Conversion Page
    </h1>
    <div>
            <button className="btn btn-danger mb-5" onClick={()=>setPage('timesweep')}>Previous Page</button> 
    </div>
    <form>

    <div className='d-flex justify-content-center align-items-center mb-5'>
      <h6>
        Fill the Value below to form the Conversion column in output CSV
      </h6>
    </div>
    <div className='d-flex justify-content-center align-items-center'>
      <div class="row g-3">
        <div className='col-2'>
          <span style={{ fontFamily: "'Cambria Math', 'TeX'" }}>1-</span>
        </div>
        <div className="col-6 mt-4" >
          <input type="text" placeholder='value' value={value} onChange={(e)=>setValue(e.target.value)} className='form-control' id="pin" name="pin" size="3" pattern="[+-]?\d+(\.\d+)?" required/>
        </div>
        <div className='col-2'>
          <span>.</span><span style={{ fontFamily: "'Cambria Math', 'TeX'" }}><i>I</i></span><sub>0</sub>/<span style={{ fontFamily: "'Cambria Math', 'TeX'" }}><i>I</i></span><sub>1</sub>
        </div>
      </div>
    </div>

    <div className='d-flex justify-content-center align-items-center mt-3'>
      <button className='btn btn-primary' onClick={handleSubmit}>Submit</button>
    </div>
    </form>
    </>
  )
}

export default ConversionPage