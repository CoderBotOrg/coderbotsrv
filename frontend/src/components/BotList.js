/* @flow */
import React from 'react'
import Bot from '../components/Bot'
import {CoderBotSrv} from '../api/CoderBotSrv'

// We can use Flow (http://flowtype.org/) to type our component's props
// and state. For convenience we've included both regular propTypes and
// Flow types, but if you want to try just using Flow you'll want to
// disable the eslint rule `react/prop-types`.
// NOTE: You can run `npm run flow:check` to check for any errors in your
// code, or `npm i -g flow-bin` to have access to the binary globally.
// Sorry Windows users :(.

// We avoid using the `@connect` decorator on the class definition so
// that we can export the undecorated component for testing.
// See: http://rackt.github.io/redux/docs/recipes/WritingTests.html
export default React.createClass({
  propTypes: {
    route: React.PropTypes.array,
    children: React.PropTypes.array
  },

  getInitialState () {
    return {
      bots: []
    }
  },

  componentDidMount () {
    var _this = this
    CoderBotSrv.getOwnBotList().then(function (bot_list) {
      _this.setState({
        bots: bot_list
      })
    })
  },

  componentWillUnmount () {
  },

  render () {
    return (
      <div className='content'>
        <div className='container-fluid'>
          <div className='row'>
            {this.state.bots.map(function (bot) {
              return (
                <Bot key={bot.uid} botName={bot.name} botLocalUrl={bot.local_url} botImage={bot.image_url}/>)
            })
          }
          </div>
        </div>
      </div>
    )
  }
})
