import React from 'react'
import WelcomePage from '../pages/WelcomePage'
import SetupPage from '../pages/SetupPage'
import ConversionPage from '../pages/ConversionPage'
import TimesweepPage from '../pages/TimesweepPage'
import InitPage from '../pages/InitPage'
import SetupGpc from '../pages/SetupGpc'
import Process from '../pages/process'
import ExpParams from '../pages/ExpParams'
import ProcessParams from '../pages/ProcessParams'
import UploadCSV from '../pages/UploadCSV'

const Routing = ({page,setPage, data, setData}) => {
  return (
    <>
            {page==='welcome' && <WelcomePage setPage={setPage} page={page} data={data} setData={setData}/>}
            {page==='setup' && <SetupPage setPage={setPage} page={page} data={data} setData={setData}/>}
            {page==='timesweep' && <TimesweepPage setPage={setPage} page={page} data={data} setData={setData}/>}
            {page==='conversion' && <ConversionPage setPage={setPage} page={page} data={data} setData={setData}/>}
            {page==='init' && <InitPage setPage={setPage} page={page} data={data} setData={setData}/>}
            {page==='setupgpc' && <SetupGpc setPage={setPage} page={page} data={data} setData={setData}/>}
            {page==='process' && <Process setPage={setPage} page={page} data={data} setData={setData}/>}
            {page==='experimentParams' && <ExpParams setPage={setPage} page={page} data={data} setData={setData}/>}
            {page==='processParams' && <ProcessParams setPage={setPage} page={page} data={data} setData={setData}/>}
            {page==='uploadCSV' && <UploadCSV setPage={setPage} page={page} data={data} setData={setData}/>}
            
            
    </>
  )
}

export default Routing