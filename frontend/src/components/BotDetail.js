import React, {PropTypes} from 'react'
import { Link } from 'react-router'
import {CoderBotSrv} from '../api/CoderBotSrv'
import {setTitle} from '../components/Title'

export default React.createClass({
  propTypes: {
    params: PropTypes.array.isRequired,
    children: PropTypes.array
  },

  getInitialState () {
    return {
      bot: {name: '', image: ''}
    }
  },

  componentDidMount () {
    var component = this
    CoderBotSrv.getBotDetail(this.props.params.botId).then(function (bot) {
      setTitle(bot.name + ' settings')
      // console.log(program_data)
      component.setState({
        bot: bot
      })
    })
  },

  handleName: function (e) {
    console.log('handleName')
    let bot = this.state.bot
    bot.name = e.target.value
    setTitle(bot.name + ' settings')
    this.setState({
      bot: bot
    })
  },

  handleImageClick: function (e) {
    console.log('handleImageClick')
    $('#i_file').click()
  },

  handleImageChange: function (e) {
    console.log('handleImageChange')
    let component = this
    let bot = this.state.bot
    let preview = $('#i_image')
    let reader = new FileReader()
    let file = e.target.files[0]
    reader.addEventListener('load', function () {
      preview.attr('src', reader.result)
      bot.image = reader.result
      component.setState({
        bot: bot
      })
    }, false)

    if (file) {
      reader.readAsDataURL(file)
    }
  },

  handleSave: function (e) {
    var component = this
    CoderBotSrv.setBotDetail(this.props.params.botId, this.state.bot).then(function (bot) {
      console.log('saved')
      component.setState({
        bot: bot
      })
    })
  },

  render () {
    return (
      <div className='col-md-12'>
        <div className='card'>
          <div className='header'>
            <h4 className='title'><input type='text'
              name='name' value={this.state.bot.name}
              onChange={this.handleName}></input></h4>
          </div>
          <div className='content'>
            <img src={this.state.bot.image} className='bot-avatar' id='i_image'
              onClick={this.handleImageClick}></img>
            <input type='file' name='image' id='i_file' className='hidden'
              onChange={this.handleImageChange}></input>
          </div>
          <div className='footer'>
            <button onClick={this.handleSave} className='btn btn-sm'>Save</button>
            <Link to='/bots' className='btn btn-sm'>
              <i className='pe-7s-refresh-2'></i>Close</Link>
          </div>
        </div>
      </div>) }
})
