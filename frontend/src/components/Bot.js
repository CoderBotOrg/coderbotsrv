import React from 'react'

export default React.createClass({
  propTypes: {
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
            <h4 className='title'>{this.props.botName}</h4>
          </div>
          <div className='content'>
            <img src={this.props.botImage} className='bot-avatar'></img>
          </div>
          <div className='footer'>
            <a href={this.props.botLocalUrl}
              target='_bot_ui'
              className='btn btn-primary btn-fill'><i className='pe-7s-plugin'></i>Open Bot UI</a>
            <a href={this.props.botLocalUrl}
              className='btn btn-fill'><i className='pe-7s-config'></i>Settings</a>
            <a href={this.props.botLocalUrl}
              className='btn btn-fill'><i className='pe-7s-airplay'></i>Sync</a>
          </div>
        </div>
      </div>) }
})
