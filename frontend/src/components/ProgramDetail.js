import React, {PropTypes} from 'react'
import {CoderBotSrv} from '../api/CoderBotSrv'
import {setTitle} from '../components/Title'

export default React.createClass({
  propTypes: {
    route: PropTypes.array,
    params: PropTypes.object,
    children: PropTypes.array
  },

  getInitialState () {
    return {
      program_data: {name: '', code: ''}
    }
  },

  componentDidMount () {
    var _this = this
    CoderBotSrv.getProgramDetail(this.props.params.programId).then(function (program_data) {
      setTitle('Program: ' + program_data.name)
      // console.log(program_data)
      _this.setState({
        program_data: program_data
      })
      // console.log(_this.state.program_data)
    })
  },

  handleProgramDetail: function (event) {
    console.log('onProgramDetail')
  },

  render () {
    console.log(this.state.program_data)
    var name = this.state.program_data.name
    var code = this.state.program_data.code
    return (
      <div className='col-md-12'>
        <div className='card'>
          <div className='header'>
            <h4 className='title'>{name}</h4>
          </div>
          <div className='content'>
            <p>{code}</p>
          </div>
          <div className='footer'>
          </div>
        </div>
      </div>) }
})
