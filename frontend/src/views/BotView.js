/* @flow */
import React, { PropTypes } from 'react'
import BotList from '../components/BotList'
import {setTitle} from '../components/Title'

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
        <BotList/>
      </div>
    )
  }
})
