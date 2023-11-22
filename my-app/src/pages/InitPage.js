import React, {useState,  useEffect} from 'react'
import Image from '../../src/assets/images/init-pic.png'
import axios from 'axios'
// import { red } from '@mui/material/colors'
const InitPage = ({page, setPage, data, setData}) => {
  const [experimentCode, setExperimentCode] = useState({text:'', set: false})
  const [selectedOption, setSelectedOption] = useState('COM1');
  const [portList, setPortList]=useState([])
  

  const MAX_NO_PORTS=32
  let temp_com_array= []
  const fetchPortList=()=>{

    for(let i=0;i<MAX_NO_PORTS+1;i++){
      temp_com_array.push(`COM${i}`)
    }
    setPortList(temp_com_array)
  }
  
  useEffect(()=>{
    fetchPortList()
  },[])
  // fetchPortList()

  const handleSelectChange = (event) => {
    setSelectedOption(event.target.value);
  };



  const addExperiment = ()=>{
    const {text} = experimentCode
    axios.post('http://localhost:5000/handle-exp', {
      port: {selectedOption},
      expName:{text}
    })
  .then(function (response) {
    setData([...data, {experimentCode: experimentCode, input: response.data.input, output: response.data.output}])
    setPage('welcome')
  })
  .catch(function (error) {
    // handle error
    console.log(error);
  })
  .finally(function () {
    // always executed
  });

  }

  const outputCsv = ()=>{

    const {text} = experimentCode
    axios.post('http://localhost:5000/handle-exp', {
      port: {selectedOption},
      expName:{text}
    })
  .then(function (response) {
    setData([...data, {experimentCode: experimentCode, input: response.data.input, output: response.data.output}])
    setPage('process')
  })
  .catch(function (error) {
    // handle error
    console.log(error);
  })
  .finally(function () {
    // always executed
  });
  }



  return (
    <>
    {/* {fetchPortList} */}
    <h1 className='mb-3'>Initialisation</h1>
    <div>
      <button className="btn btn-danger mb-5" onClick={()=>setPage('conversion')}>Previous Page</button>
    </div>
    <div className='d-flex justify-content-center align-items-center'>
      <img alt='init-pic' src={Image} className='mb-5 img-fluid w-70 ' />
    </div>



    <div className='row'>
      <div className='col-8'>
          <div style={{}} className="input-group mb-2 ">
            <div className="input-group-prepend">
              <span className="input-group-text" id="">Experiment Code</span>
            </div>
            <input  type="text" class="form-control" onChange={(e)=>setExperimentCode({set:false, text: e.target.value})}/>
          </div>
      </div>
      <div className='col-4'>
          <select class="form-select" aria-label="Default select example" value={selectedOption} onChange={handleSelectChange}>
            {
            portList.map(
              port=><option value={port}>{port}</option>
            )
            }
            
          </select>
      </div>
    </div>
    <div  className='d-flex justify-content-center align-items-center'>
      <button className='btn btn-success w-25 mb-5'  onClick={()=>experimentCode.text&&setExperimentCode({...experimentCode, set:true})}>
        OK
      </button>
    </div>






    {experimentCode['set'] && 
    <div className='row m-4'>
      <div className='col-8'>
        <h5>
          Name the experiment ({experimentCode.text}) in the Spinsolve software
        </h5>
        <h6>
          Spinsolve Check
        </h6>
      </div>
      <div className='col-4'>
        <button className = 'btn btn-success ml-2' >
          OK
        </button>
        <button style={{marginLeft:'5px'}} className = 'btn btn-warning' >
          Help
        </button>
      </div>
    </div>}
    
    <div className='d-flex justify-content-center align-items-center'>
      {/* <button className='btn btn-warning p-3 w-25' onClick={addExperiment} disabled={!experimentCode.set}>
        Continue
      </button> */}
    </div>

    <div className='d-flex justify-content-center align-items-center mt-3'>
      <button className='btn btn-success p-3 w-25' onClick={outputCsv} disabled={!experimentCode.set}> 
        Finish
      </button>
    </div>
    {/* {experimentCode.set&&<>
    {experimentCode.text}
    </>} */}


    </>
  )
}

export default InitPage