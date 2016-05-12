import React from 'react'
import Title from '../components/Title'

export default React.createClass({
  propTypes: {
    children: React.PropTypes.array
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
      <nav className='navbar navbar-default navbar-fixed'>
        <div className='container-fluid'>
          <div className='navbar-header navbar-right'>
            <button type='button' className='navbar-toggle' data-toggle='collapse' data-target='#sidebar'>
              <span className='sr-only'>Toggle navigation</span>
              <span className='icon-bar'></span>
              <span className='icon-bar'></span>
              <span className='icon-bar'></span>
            </button>
            <Title/>
          </div>
        </div>
      </nav>) }
})
