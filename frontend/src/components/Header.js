import React from 'react'
import Title from '../components/Title'

export default React.createClass({
  propTypes: {
    children: React.PropTypes.array
  },

  render () {
    return (
      <nav className='navbar navbar-default navbar-fixed'>
        <div className='container-fluid'>
          <div className='navbar-header navbar-left'>
            <button type='button' className='navbar-toggle' data-toggle='collapse' data-target='#example-2'>
              <span className='sr-only'>Toggle navigation</span>
              <span className='icon-bar'></span>
              <span className='icon-bar'></span>
              <span className='icon-bar'></span>
            </button>
            <Title/>
          </div>
          <div className='collapse navbar-collapse'>
            <ul className='nav navbar-nav navbar-right'>
              <li>
                <div id='gitkit'></div>
              </li>
            </ul>
          </div>
        </div>
      </nav>) }
})
