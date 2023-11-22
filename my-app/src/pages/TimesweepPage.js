import React, {useState} from 'react'
import TimesweepSlider from '../components/Slider'
import Constants from '../util/Constants'
import image from '../../src/assets/images/timesweeps.png'
import axios from 'axios'
const TimesweepPage = ({setPage, page}) => {
  var {reactorVolume} = Constants
  reactorVolume = 10000
  console.log('reactorVol', reactorVolume)
  const [value, setValue] = useState([10, 20])
  const [error, setError] = useState('')
  const [savedTimesweep, setSavedTimesweep] = useState([])
  const [filename, setFilename] = useState('')
  const calcFlowRates = (fromTimesweep, toTimesweep) => {
    const fromFlowRate = parseFloat(REACTOR_VOLUME) / parseFloat(value[0])
    const toFlowRate = parseFloat(REACTOR_VOLUME) / parseFloat(value[1])
    return [fromFlowRate, toFlowRate]
  }
  const handleTimesweep = (e) =>{
    e.preventDefault()
    if(savedTimesweep.length > 0){

      let lastTimesweep = savedTimesweep[savedTimesweep.length-1]
      console.log(value[0])

      if (parseFloat(value[0]) !== parseFloat(value[1]) && parseFloat(value[0]) > 0 && parseFloat(value[1]) > 0 && parseFloat(value[0]) === parseFloat(lastTimesweep['end'])){
        setError('')
        console.log('pass')
        setSavedTimesweep([...savedTimesweep, {start: value[0], end:value[1], startFR: calcFlowRates(value[0], value[1])[0], endFR: calcFlowRates(value[0], value[1])[1] }])
      }
      else{
        setError('Wrong Range of start and end Timesweep')
      }
    }
    else{

      if (parseFloat(value[0]) !== parseFloat(value[1]) && parseFloat(value[0]) > 0 && parseFloat(value[1]) > 0){
        setError('')
        console.log('pass')
        setSavedTimesweep([...savedTimesweep, {start: value[0], end:value[1], startFR: calcFlowRates(value[0], value[1])[0], endFR: calcFlowRates(value[0], value[1])[1] }])
      }
      else{
        setError('Invalid Range of start and end Timesweep')
      }
    }
  }

  const deleteTimesweep = (index) => {
    // e.preventDefault()
    console.log('index', index)
    setSavedTimesweep(savedTimesweep.filter((item,i)=>(i!==index)))
  } 

  const REACTOR_VOLUME = 0.9
  const handleSubmit = (e) => {
    e.preventDefault()
    if(filename){

      axios.post('http://localhost:5000/inputcsv', {
          timesweeps : savedTimesweep,
          filename : filename
      })
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error)
      });
  
  
      setPage('conversion')
    }
    else{
      setError('Filename cannot be empty!')
    }
  }

  return (
    <>
    <h1>Timesweeps</h1>
    <div>
      <button className="btn btn-danger mb-5" onClick={()=>setPage('setup')}>Previous Page</button>
    </div>
    <div className='d-flex justify-content-center align-items-center'>
    <img alt='timesweeps-img' src={image} className='mb-5 img-fluid w-75 w-sm-150 w-lg-100' />
    </div>
    <TimesweepSlider value={value} setValue={setValue}/>
  <form style={{marginTop: 50}}>

    <div className='d-flex justify-content-center'>

      <div class="input-group w-50">
        <div class="input-group-prepend">
          <span class="input-group-text" id="inputGroup-sizing-default">From (min)</span>
        </div>
        <input type="number" class="form-control" aria-label="Default" aria-describedby="inputGroup-sizing-default" value={value[0]} onChange={(e)=> setValue([e.target.value, value[1]])}/>
      </div>
    </div>
      <br/>
    <div className='d-flex justify-content-center'>
      <div class="input-group w-50">
        <div class="input-group-prepend">
          <span class="input-group-text" id="inputGroup-sizing-default">End (min)</span>
        </div>
        <input type="number" class="form-control" aria-label="Default" aria-describedby="inputGroup-sizing-default" value={value[1]} onChange={(e)=> setValue([value[0], e.target.value])}/>
      </div>
    </div>
    <div className='d-flex justify-content-center'>
      <input className='btn btn-success mt-4 mb-4' value='Add' type='button' style={{width:100}} onClick={handleTimesweep} />
    </div>
    


    {error&&<div className='d-flex justify-content-center mt-4' style={{color: 'red', fontSize: 10}}>{error}</div>}

    {
      savedTimesweep.map((item, index)=> (
        <>
      <div className='d-flex justify-content-center align-items-center'>
      <div className="card" style={{width: '75%'}}>
      <div className="card-header d-flex justify-content-center" >
        <div>
          Timesweep <span style={{color:'red'}}>#{index+1}</span>
        </div>
      </div>
      <ul className="list-group list-group-flush">
        <li class="list-group-item">
          <div className='d-flex  justify-content-around'>

            <div style={{padding:10}}>
              <i>Timesweep Start</i>
            </div>
            <div style={{padding:10}}>
              {item['start']} minutes 
            </div>
          </div>
             
        </li>
        <li class="list-group-item">
            {/* Timesweep end {item['end']} minute   */}
            <div className='d-flex justify-content-around'>

              <div style={{padding:10}}>
              <i>Timesweep End</i>
              </div>
              <div style={{padding:10}}>
                {item['end']} minutes 
              </div>
            </div>
        </li>
        <li class="list-group-item">
            {/* Flowrate start {item['startFR'].toFixed(2)} minute   */}            
            <div className='d-flex justify-content-around'>

              <div style={{padding:10}}>
              <i>Flowrate Start</i>
              </div>
              <div style={{padding:10}}>
              {item['startFR'].toFixed(2)} Minutes
              </div>
            </div>
            
        
        </li>
        <li class="list-group-item">

            {/* Flowrate end {item['endFR'].toFixed(2)} minute*/}             
            <div className='d-flex justify-content-around'>

              <div style={{padding:10}}>
              <i>Flowrate End</i>
              </div>
              <div style={{padding:10}}>
              {item['endFR'].toFixed(2)} Minutes
              </div>
            </div>
        </li>
      </ul>
      </div>
      </div>
      <div className='d-flex justify-content-center'>
        <input type='button' value='Delete' className="btn btn-danger mt-4 justify-self-center p- " onClick={()=>deleteTimesweep(index)}/>
      </div>
      <br/>


      </>
      ))
      

    }

    {savedTimesweep.length > 0 &&
    <>

      <div className='d-flex justify-content-center align-items-center'>
        <div>
          <div class="form-group">
            <input type="text" class="form-control mb-4" value={filename} onChange={(e)=>setFilename(e.target.value)} placeholder="CSV filename (xxx.csv)" required/>
            {error&&<p style={{color: 'red', fontSize: '15px'}}>{error}</p>}
          </div>
        </div>
      </div>
      <div className='d-flex justify-content-center align-items-center'>
        <input className='btn btn-primary w-50 mb-5' type='submit' value='Submit' onClick={handleSubmit} />
      </div>

    </>
      
    }
  </form>
    

    </>
  )
}

export default TimesweepPage