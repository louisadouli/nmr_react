import React, {useState, useEffect} from 'react'
import axios from 'axios'
// import "font-awesome/css/font-awesome.min.css"
const Process = ({page, setPage}) => {
  const [showGraphButton, setShowGraphButton] = useState(false)
  const [data, setData] = useState([])
  const [newData, setNewData] = useState({port:'', expName:'', file:''})
  const [editItem, setEditItem] = useState('')
  const editExperiment= (item, e) =>{
    setEditItem('')
    // e.preventDefault()
    axios.post('http://localhost:5000/edit-exp', {
      data: data
    })
    .then(function (response) {
      console.log('response', response)
    })
    .catch(function (error) {
      console.log(error);
    });

  }
  const removeExperiment = (item, e) => {
    e.preventDefault()
    axios.post('http://localhost:5000/remove-exp', {
      i: item.index
    })
    .then(function (response) {
      const {files, ports, expNames} = response.data.data  
      const arr=[]
      ports.forEach((element, index) => {
        arr.push({index: index+1, file:files[index], port: ports[index], expName: expNames[index]})

      });
      setData(arr)
    })
    .catch(function (error) {
      console.log(error);
    });
  }
  const clearFiles = ()=>{
    axios.get('http://localhost:5000/clear')
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
  }
  const creategraph=()=>{
    axios.get('http://localhost:5000/creategraph')
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
  }
  const run=()=>{
 
    axios.get('http://localhost:5000/outputcsv')
    .then(function (response) {
      console.log(response);
      setShowGraphButton(true)
    })
    .catch(function (error) {
      console.log(error);
    });


  }
  useEffect(() => {
        axios.get('http://localhost:5000/getcsvfiles')
        .then(function (response) {
          
          // handle success
          // console.log(response.data);
          const {files, ports, expNames} = response.data
          // for(let i; i < ports.length; i++){
          //   console.log('i', i)  
          // }     
          const arr=[]
          ports.forEach((element, index) => {
            arr.push({index: index+1, file:files[index], port: ports[index], expName: expNames[index]})

          });
          setData(arr)
          // console.log('ports', ports.length)
          // setData({files, ports, expNames})
        })
        .catch(function (error) {
          // handle error
          console.log(error);
        })
        .finally(function () {
          // always executed
        });
        return () => {
        };
    }, []);


    const updatePort = (id, newPort) => {
      console.log(id)
      const index = data.findIndex(obj=>obj.index==id)
      const updatedArray = [...data]
      updatedArray[index] = {...updatedArray[index], port:newPort}
      setData(updatedArray)
    }

    const updateExpCode = (id, newCode) => {
      console.log(id)
      const index = data.findIndex(obj=>obj.index==id)
      const updatedArray = [...data]
      updatedArray[index] = {...updatedArray[index], expName:newCode}
      setData(updatedArray)
    }
    return (
    <>
        <h1 className='mb-3'>Process</h1>
        <div>
            <button className="btn btn-danger mb-5" onClick={()=>setPage('init')}>Previous Page</button>
        </div>
        {console.log(data)}


 {
data &&
<>
<table class="table">
  <thead class="thead-dark">
    <tr>
      <th scope="col">#</th>
      <th scope="col">Files</th>
      <th scope="col">Experiment Code</th>
      <th scope="col">Ports</th>
      <th scope="col">Action</th>
    </tr>
  </thead>
  <tbody>
    {console.log('data', data)}
  {
    data.map(item=>(
    <>
    <tr key={item.index}>
      <th scope="row">{item.index}</th>
      <td>{item.file}</td>
      <td>{item.expName}</td>
      <td>{item.port}</td>
      {/* <td>{item.index}</td> */}
      <td>
        <button className='btn btn-danger' style={{marginLeft: '10%', ackgroundColor: 'red'}} onClick={(e)=>removeExperiment(item, e)} >
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
          <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5Zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5Zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6Z"/>
          <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1ZM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118ZM2.5 3h11V2h-11v1Z"/>
        </svg> 
        </button>  

        {/* <button type="button" class="btn btn-primary" onClick={()=>{
          if(editItem){
            setEditItem('')
          }
          else{

            setEditItem(item.index)
          }
        }}>
          Edit
        </button>       */}
          
        </td>

    </tr>
    <tr>

    {
          editItem===item.index &&
          <div style={{margin: 50}}>
              <form >

                  <div className="col">
                    <label for="experimentCode" class="form-label" style={{fontSize: '25px'}}>Experiment Code</label>
                    <input type="text" class="form-control" id="experimentCode" aria-describedby="experimentCode" value={item.expName} onChange={(e)=>updateExpCode(item.index, e.target.value)}/>
                  </div>
                  <div className="col" style={{width: 300}} >
                    <label for="port" class="form-label" style={{fontSize: '25px'}}>Port</label>
                    <input type="text" class="form-control" id="port" value={item.port} onChange={(e)=>updatePort(item.index, e.target.value)}/>
                  </div>
                  <div class>
                    <button type="submit" class="btn btn-primary" onClick={editExperiment}>Submit</button>
                  </div>
                
              </form>
          </div>
        }
    </tr>
   
    </>
    ))
  }
  </tbody>
</table>

<div>
  <button className='btn btn-danger' onClick={run}>Connect to Syrenge Pump(s)</button>
  {/* <button className='btn btn-danger' onClick={clearFiles}>Clear</button> */}

  {
  showGraphButton&&
  <button className="btn btn-danger" onClick={creategraph}>Save Graphs</button>
  }

</div>
</>
} 
    </>
  )
}

export default Process