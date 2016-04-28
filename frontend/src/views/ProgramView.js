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

  componentDidMount () {
    setTitle(this.props.route.title)
    var component = this
    CoderBotSrv.getEvents().then(function (events) {
      console.log(events)
      if (events.length) {
        component.forceUpdate()
      }
    })
  },

  render () {
    return (
      <div>
        <ProgramList status={CoderBotSrv.PROGRAM_STATUS_PRIVATE}/>
      </div>
    )
  }
})
