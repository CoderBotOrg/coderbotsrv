/* @flow */
import React, { PropTypes } from 'react'
import BotDetail from '../components/BotDetail'
import {setTitle} from '../components/Title'

export default React.createClass({
  propTypes: {
    botId: PropTypes.object,
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
        <BotDetail {...this.props}/>
      </div>
    )
  }
})
