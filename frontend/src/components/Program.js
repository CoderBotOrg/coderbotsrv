import React from 'react'
import { Link } from 'react-router'

export default React.createClass({
  propTypes: {
    programName: React.PropTypes.string.isRequired,
    programImage: React.PropTypes.string,
    programId: React.PropTypes.string,
    children: React.PropTypes.array
  },

  render () {
    var link_to = '/programs/detail/' + this.props.programId
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
            <Link className='btn btn-primary btn-fill' to={link_to}>Program Detail</Link>
          </div>
        </div>
      </div>) }
})
