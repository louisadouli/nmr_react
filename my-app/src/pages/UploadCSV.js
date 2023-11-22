import React, {useState} from 'react'
import axios from 'axios';
const UploadCSV = ({page, setPage}) => {
    const [file, setFile] = useState(null);

    const handleFileChange = (e) => {
      setFile(e.target.files[0]);
    };
  
    const handleFormSubmit = (e) => {
      e.preventDefault();
  
      // Create a FormData object
      const formData = new FormData();
      formData.append('file', file);
  
    //   // Send the form data to the backend using fetch
      fetch('http://localhost:5000/uploadcsv', {
        method: 'POST',
        body: formData
      })
        .then(response => response.json())
        .then(data => {
        //   console.log(data);
          setPage('processParams')
          // Handle the response from the backend as needed
        })
        .catch(error => console.error(error));




    };
  
    return (
        <div style={{marginTop:'40%'}}>
            <form onSubmit={handleFormSubmit}>
                <div className='d-flex justify-content-center align-items-center'>
                    <input type="file" className='btn btn-success' onChange={handleFileChange} />
                </div>
                <div className='d-flex justify-content-center align-items-center m-4'>
                    <button className='btn btn-primary' type="submit">Upload</button>
                </div>
            </form>
        </div>
    );
}

export default UploadCSV