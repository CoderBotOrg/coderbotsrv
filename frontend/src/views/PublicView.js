/* @flow */
import React, { PropTypes } from 'react'

export default React.createClass({
  propTypes: {
    route: PropTypes.array,
    children: PropTypes.array
  },

  componentDidMount () {
    window.google.identitytoolkit.signInButton(
      '#gitkit', // accepts any CSS selector
      {
        widgetUrl: '/auth/login',
        signOutUrl: '/auth/logout',
        // Optional - Begin the sign-in flow in a popup window
        popupMode: true
      }
    )
  },

  render () {
    return (
      <div className='wrapper'>
        <div className='content'>
          <div className='container-fluid'>
            <div className='col-md-6 col-sm-6 col-md-offset-2 col-sm-offset-3'>
              <h1>Welcome to CoderBot</h1>
              <p>Please signup</p>
              <div id='gitkit'></div>
            </div>
          </div>
        </div>
      </div>
    )
  }
})
