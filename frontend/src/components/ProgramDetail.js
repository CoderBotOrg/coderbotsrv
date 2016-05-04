import React, {PropTypes} from 'react'
import {CoderBotSrv} from '../api/CoderBotSrv'
import {setTitle} from '../components/Title'
// import {Blockly} from '../static/js/blockly/blockly_compressed'

var inject_once = true

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
    CoderBotSrv.getProgramDetail(this.props.params.programId).then(function (program_data) {
      setTitle('Program: ' + program_data.name)
      // console.log(program_data)
      component.setState({
        program_data: program_data
      })
      if (inject_once) {
        inject_once = false
        // Blockly.inject(document.getElementById('blocklyDiv'),
        //   {path: '../../', toolbox: document.getElementById('toolbox'),
        //   scrollbars: true, maxBlocks: -1})
        // $('.blocklyToolboxDiv').appendTo('#page-program')
        // $('.blocklyTooltipDiv').appendTo('#page-program')
        // $('.blocklyWidgetDiv').appendTo('#page-program')
      }

      // console.log(_this.state.program_data)
    })
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
            <div className='code' id='blocklyDiv'>{code}</div>
          </div>
          <div className='footer'>
          </div>
        </div>
      </div>) }
})
