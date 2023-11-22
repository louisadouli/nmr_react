import './App.css';
import React, {useState} from 'react'
import ProgressBar from "./components/ProgressBar";
import Routing from './components/Routing';
function App() {
  const [page, setPage] = useState("welcome")
  const [data, setData] = useState([])
  return (
    <div className="App">
      <h1>
        <div className='container mt-4'>
          <div className='mb-4'>
            <ProgressBar page={page}/>
          </div>
          <div className='mt-4'>
            <Routing page={page} setPage={setPage} data={data} setData={setData}/>
          </div>
        </div>
      </h1> 
    </div>

  );
}

export default App;
