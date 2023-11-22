import React, {useState} from 'react'
import Menu from '../components/pages/welcome/Menu'
// import { FolderPicker, IFolder } from "@pnp/spfx-controls-react/lib/FolderPicker";
const WelcomePage = ({page, setPage}) => {
  const [selectedFolder, setSelectedFolder] = useState('');
  const handleFolderSelect = (event) =>{
    event.preventDefault()
    const folderPath = event.target;
    setSelectedFolder(folderPath);
    console.log('folderPath', folderPath)
      
  }
  return (
    <>
      <div>
        <div className='d-flex justify-content-center'>
          WelcomePage
        </div>   
        <Menu setPage={setPage}/>
        <div>
      {/* <input type="file" webkitdirectory="true" onChange={handleFolderSelect} />
      {selectedFolder && (
        <p>The selected folder is located at: {selectedFolder}</p>
      )} */}
    </div>


      </div>
    </>
  )
}

export default WelcomePage