/* @flow */
import React, { PropTypes } from 'react'
import ProgramDetail from '../components/ProgramDetail'
import {setTitle} from '../components/Title'

export default React.createClass({
  propTypes: {
    programId: PropTypes.object,
    route: PropTypes.string,
    params: PropTypes.object,
    children: PropTypes.array
  },

  componentDidMount () {
    setTitle(this.props.route.title)
  },

  render () {
    return (
      <div>
        <ProgramDetail {...this.props}/>
      </div>
    )
  }
})
