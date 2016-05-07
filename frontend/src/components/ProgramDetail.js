import React, {PropTypes} from 'react'
import {CoderBotSrv} from '../api/CoderBotSrv'
import {setTitle} from '../components/Title'
import {BlocklyWorkspace} from '../static/js/blockly/blockly'

// var inject_once = true

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
    var component = this
    console.log('Blockly.inject')
    this.bw = new BlocklyWorkspace('blocklyDiv', 'toolbox')
    CoderBotSrv.getProgramDetail(this.props.params.programId).then(function (program_data) {
      setTitle('Program: ' + program_data.name)
      // console.log(program_data)
      component.setState({
        program_data: program_data
      })
      console.log('Blockly.load program code')
      component.bw.load(program_data.dom_code)
    })
  },

  componentWillUnmount () {
    console.log('Blockly.clear program code')
    this.bw.clear()
  },

  handleProgramDetail: function (event) {
    console.log('onProgramDetail')
  },

  render () {
    let name = this.state.program_data.name
    let code = this.state.program_data.code
    return (
      <div className='col-md-12'>
        <div className='card'>
          <div className='header'>
            <h4 className='title'>{name}</h4>
          </div>
          <div className='content' id='blockly'>
            <div id='blocklyDiv'></div>
            <div id='toolbox'></div>
            <div className='code'>{code}</div>
          </div>
          <div className='footer'>
          </div>
        </div>
      </div>) }
})
