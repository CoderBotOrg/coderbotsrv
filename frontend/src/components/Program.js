import React from 'react'

export default React.createClass({
  propTypes: {
    programName: React.PropTypes.string.isRequired,
    programImage: React.PropTypes.string,
    programUrl: React.PropTypes.string,
    children: React.PropTypes.array
  },

  render () {
    return (
      <div className='col-md-4'>
        <div className='card'>
          <div className='header'>
            <h4 className='title'>{this.props.programName}</h4>
          </div>
          <div className='content'>
            <img src={this.props.programImage}></img>
          </div>
          <div className='footer'>
            <a href={this.props.programUrl}
              className='btn btn-primary btn-fill'>Look inside</a>
          </div>
        </div>
      </div>) }
})
