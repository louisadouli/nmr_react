import React from 'react'

const TabInput = ({title, value, handleChange}) => {
  return (
    <div className='row mt-5 d-flex justify-content-center align-items-center'>
      <div className='col-8 col-md-4'>
        <div class="input-group">
          <div class="input-group-prepend">
            <span class="input-group-text" id="">{title}</span>
          </div>
          <input type="number" class="form-control" value={value}  onChange={handleChange}/>
        </div>
      </div>
    </div>
  )
}

export default TabInput