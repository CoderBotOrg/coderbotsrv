/* @flow */
import React, { PropTypes } from 'react'
import { Link } from 'react-router'
import {setTitle} from '../components/Title'

export default React.createClass({
  propTypes: {
    // route: PropTypes.array,
    children: PropTypes.array
  },

  componentDidMount () {
    setTitle('Home Page')
  },

  render () {
    return (
      <div>
        <h2>Home Page</h2>
        <p>Use this site to:</p>
        <ul>
          <li>Have <Link to='/bots'>access to your CoderBot(s)</Link> when connected
          to your local (Home or School) wifi netwok</li>
          <li>Browse <Link to='/programs'>your programs</Link> saved in the cloud
          storage</li>
          <li>[Coming soon] Browse <Link to='/library'>existing public
          programs</Link></li>
        </ul>
      </div>
    )
  }
})
