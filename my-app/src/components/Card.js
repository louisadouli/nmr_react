import React from 'react'

const Card = ({title, text, setPage}) => {
  return (
    <>
      <div className='option-menu'>
        <div className="card" style={{border: 'none'}}>
          <div className='p-3' style={{height:'175px', borderRadius: 10, border: 'solid #0D6EFD'}}>
            <div className="card-body">
              <h4 className="card-title">{title}</h4>
              <p className="card-text" style={{fontSize: 15}}>{text}</p>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

export default Card