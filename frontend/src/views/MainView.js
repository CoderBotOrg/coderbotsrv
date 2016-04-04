/* @flow */
import React, { PropTypes } from 'react'
import SideNav from '../components/SideNav'
import SideMenuItem from '../components/SideMenuItem'
import Header from '../components/Header'
import HomeView from '../views/HomeView'

export default React.createClass({
  propTypes: {
    route: PropTypes.array,
    children: PropTypes.array
  },

  render () {
    return (
      <div className='wrapper'>
        <SideNav brandName='CoderBot' brandImage='/static/img/coderbot_logo_79.png'>
          <SideMenuItem to='/bots' destLabel='My CoderBot(s)' iconClassName='pe-7s-plugin'/>
          <SideMenuItem to='/programs' destLabel='My Programs' iconClassName='pe-7s-drawer'/>
          <SideMenuItem to='/library' destLabel='Public Programs' iconClassName='pe-7s-cloud'/>
        </SideNav>
        <div className='main-panel'>
          <Header/>
          <div className='content'>
            <div className='container-fluid'>
              {(() => {
                if (this.props.children) {
                  return this.props.children
                } else {
                  return (<HomeView/>)
                }
              })()}
            </div>
          </div>
        </div>
      </div>
    )
  }
})
