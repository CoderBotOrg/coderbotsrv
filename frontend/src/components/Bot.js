import React from 'react'
import { Link } from 'react-router'

export default React.createClass({
  propTypes: {
    botId: React.PropTypes.string.isRequired,
    botName: React.PropTypes.string.isRequired,
    botImage: React.PropTypes.string,
    botLocalUrl: React.PropTypes.string,
    children: React.PropTypes.array
  },

  render () {
    return (
      <div className='col-md-4'>
        <div className='card'>
          <div className='header'>
            <h4 className='title'><a href={this.props.botLocalUrl}
              target='_bot_ui'>{this.props.botName}</a></h4>
          </div>
          <div className='content'>
            <a href={this.props.botLocalUrl}
              target='_bot_ui'><img src={this.props.botImage} className='bot-avatar'></img></a>
          </div>
          <div className='footer'>
            <a href={this.props.botLocalUrl}
              target='_bot_ui'
              className='btn btn-primary btn-sm'><i className='pe-7s-plugin'></i>Open Bot UI</a>
            <Link to={'/bots/' + this.props.botId}
              className='btn btn-sm'><i className='pe-7s-config'></i>Settings</Link>
            <button href={this.props.botLocalUrl}
              className='btn btn-sm'><i className='pe-7s-refresh-2'></i>Sync</button>
          </div>
        </div>
      </div>) }
})
