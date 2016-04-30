/* @flow */
import React, { PropTypes } from 'react'
import ProgramList from '../components/ProgramList'
import {setTitle} from '../components/Title'
import {CoderBotSrv} from '../api/CoderBotSrv'

export default React.createClass({
  propTypes: {
    route: PropTypes.array,
    children: PropTypes.array
  },

  updateProgList (component, events) {
    console.log(events)
    if (events.length) {
      component.forceUpdate()
    }
    CoderBotSrv.getEvents().then(function (events) { component.updateProgList(component, events) })
  },

  componentDidMount () {
    setTitle(this.props.route.title)
    var component = this
    this.updateProgList(component, [])
  },

  render () {
    return (
      <div>
        <ProgramList status={CoderBotSrv.PROGRAM_STATUS_PRIVATE}/>
      </div>
    )
  }
})
