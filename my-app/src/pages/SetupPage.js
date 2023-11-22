import React, {useState} from 'react'
import image from '../../src/assets/images/setup-pic.png'
import axios from 'axios'
const SetupPage = ({page, setPage}) => {
  const [inputValues, setInputValues] = useState({reactorVol:'0.9', dv1:'0.43', nmrInterval:'17', sta:'1.3'});
  const handleSubmit = (e) =>{
    e.preventDefault()

    axios.post('http://localhost:5000/setup', {
        reactorVol: inputValues['reactorVol'], 
        dv1: inputValues['dv1'],
        nmrInterval: inputValues['nmrInterval'], 
        sta: inputValues['sta'],
      
    })
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error)
    });


    setPage('timesweep')
  }
  return (
    <>
    <h1>Setup Page</h1>
    <div>
      <button className="btn btn-danger" onClick={()=>setPage('welcome')}>Previous Page</button>
    </div>

        <img alt='setup-img' src={image} className='mb-5 img-fluid w-100 w-sm-150 w-lg-50' />
   <div className='row'>
      <div className='col-5'>
        <div className="input-group">
          <div className="input-group-prepend">
            <span className="input-group-text" id="">Reactor Volume</span>
          </div>
          <input type="text" className="form-control" value={inputValues['reactorVol']} onChange={(e)=>setInputValues({...inputValues, reactorVol:e.target.value})}/>
        </div>
      </div>
      <div className='col-1'><p style={{fontSize:'20px'}} className='mt-1'>ml</p></div>
      <div className='col-5'>
        <div className="input-group">
          <div className="input-group-prepend">
            <span className="input-group-text" id="">Dead Volume 1</span>
          </div>
          <input type="text" className="form-control" value={inputValues['dv1']} onChange={(e)=>setInputValues({...inputValues, dv1:e.target.value})}/>
        </div>
      </div>
      <div className='col-1'><p style={{fontSize:'20px'}} className='mt-1'>ml</p></div>
    </div>

    <div className='row mt-4'>
      <div className='col-5'>
        <div className="input-group">
          <div className="input-group-prepend">
            <span className="input-group-text" id="">NMR Interval</span>
          </div>
          <input type="text" className="form-control" value={inputValues['nmrInterval']} onChange={(e)=>setInputValues({...inputValues, nmrInterval:e.target.value})}/>
        </div>
      </div>
      <div className='col-1'><p style={{fontSize:'20px'}} className='mt-1'>Sec</p></div>
      <div className='col-5'>
        <div className="input-group">
          <div className="input-group-prepend">
            <span className="input-group-text" id="">Stabilization Factor</span>
          </div>
          <input type="text" className="form-control" value={inputValues['sta']} onChange={(e)=>setInputValues({...inputValues, sta:e.target.value})}/>
        </div>
      </div>
      <div className='col-1'><p style={{fontSize:'20px'}} className='mt-1'>X</p></div>
    </div>

    <div className='d-flex justify-content-center'>
    <input className='btn btn-success m-4' value='Confirm' type='submit' onClick={handleSubmit}/>
    <input className='btn btn-primary m-4' value='Reaction Solution' type='button'/>
    </div>

    </>
    )

  

  
  
}

export default SetupPage