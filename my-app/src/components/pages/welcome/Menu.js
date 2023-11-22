import React from 'react'
import Card from '../../Card'
import axios from 'axios'

const Menu = ({setPage}) => {

  const nmrAction =() =>{

    setPage('setup')
    axios.post('http://localhost:5000/setexperiment', {
      experimentType: 'NMR'   
    })
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
  }
  
  const gpcAction=()=>{
    setPage('setupgpc')
    axios.post('http://localhost:5000/setexperiment', {
      experimentType: 'NMR-GPC'
    })
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
  }
  return (
    <>
    <div className="row mt-5">
        <div className="cards col-sm-6" onClick={nmrAction}>
            <Card title='NMR' text=' analyze the chemical and physical properties of molecules' setPage={setPage}/>
        </div>
        <div className="col-sm-6" onClick={gpcAction}>
              <Card title='NMR - GPC' text='combination of NMR and GPC used to analyze the chemical structure and molecular weight distribution of polymers.' setPage={setPage}/>
        </div>
    </div>
    </>
  )
}

export default Menu