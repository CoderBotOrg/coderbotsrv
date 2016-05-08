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
    this.bw = new BlocklyWorkspace('blocklyDiv', 'blocklyToolbox')
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

  handleName: function (event) {
    let program_data = this.state.program_data
    program_data.name = event.target.value
    setTitle(program_data.name + ' details')
    this.setState({
      program_data: program_data
    })
  },

  handleSetPublic (event) {
    let program_data = this.state.program_data
    program_data.status = CoderBotSrv.PROGRAM_STATUS_PUBLIC
    this.setState({
      program_data: program_data
    })
  },

  handleSetPrivate (event) {
    let program_data = this.state.program_data
    program_data.status = CoderBotSrv.PROGRAM_STATUS_PRIVATE
    this.setState({
      program_data: program_data
    })
  },

  handleTags (event) {
    let program_data = this.state.program_data
    let taglist = event.target.value.split(',')
    program_data.tags = taglist.map(function (tag) { return tag !== '' ? $.trim(tag) : null })
    this.setState({
      program_data: program_data
    })
  },

  handleSave (event) {
    CoderBotSrv.setProgramDetail(this.state.program_data.uid, this.state.program_data)
    console.log('saved')
  },

  handleDelete (event) {
    let program_data = this.state.program_data
    program_data.status = CoderBotSrv.PROGRAM_STATUS_DELETED
    CoderBotSrv.setProgramDetail(this.state.program_data.uid, program_data)
    console.log('deleted')
  },

  render () {
    let pubButtonClass = 'btn' +
      (this.state.program_data.status === CoderBotSrv.PROGRAM_STATUS_PRIVATE ? '' : ' hidden')
    let priButtonClass = 'btn' +
      (this.state.program_data.status === CoderBotSrv.PROGRAM_STATUS_PUBLIC ? '' : ' hidden')
    return (
      <div className='col-md-12'>
        <div className='card'>
          <div className='header'>
            <h4 className='title'><input type='text'
              name='name' value={this.state.program_data.name}
              onChange={this.handleName}></input></h4>
          </div>
          <div className='content blockly-area' id='blocklyArea'>
            <div id='blocklyDiv' className='blockly-workspace'></div>
            <div id='blocklyToolbox' className='hidden'></div>
          </div>
          <div className='footer'>
            <div className='input-group'>
              <input type='text' className='form-control' name='tags' value={this.state.program_data.tags}
                placeholder='tags, ...' onChange={this.handleTags}/>
            </div>
            <div className='input-group'>
              <button className={pubButtonClass} onClick={this.handleSetPublic}>Set as Public</button>
              <button className={priButtonClass} onClick={this.handleSetPrivate}>Set as Private</button>
              <button className='btn btn-primary' onClick={this.handleSave}>Save</button>
              <button className='btn' onClick={this.handleDelete}>Delete</button>
            </div>
          </div>
        </div>
      </div>) }
})
