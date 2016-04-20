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
  },

  render () {
    return (
      <div>
        <ProgramList status={CoderBotSrv.PROGRAM_STATUS_PUBLIC}/>
      </div>
    )
  }
})
