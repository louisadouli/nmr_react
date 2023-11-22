import React from 'react'
import Card from '../components/Card'
const ExpParams = ({page, setPage}) => {
  return (
    <>

<>
    <div className="row mt-5">
        <div className="cards col-sm-6" onClick={()=>{setPage('init')}}>
            <Card title='Using One Syringe pump' text=' analyze the chemical and physical properties of molecules' setPage={setPage}/>
        </div>
        <div className="col-sm-6" onClick={()=>{setPage('uploadCSV')}}>
              <Card title='Using 3-4 Syringe pump' text='combination of NMR and GPC used to analyze the chemical structure and molecular weight distribution of polymers.' setPage={setPage}/>
        </div>
    </div>

    </>
        
    </>
  )
}

export default ExpParams