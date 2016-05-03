import React from 'react'
import { IndexLink } from 'react-router'

export default React.createClass({
  propTypes: {
    brandName: React.PropTypes.string.isRequired,
    brandImage: React.PropTypes.string.isRequired,
    children: React.PropTypes.array
  },

  render () {
    return (
      <div className='sidebar' data-color='azure' data-image='/static/img/sidebar-1.jpg'>
        <div className='sidebar-wrapper'>
          <div className='logo'>
            <IndexLink to='/'>
              <img src={this.props.brandImage}/>
              <span>{this.props.brandName}</span>
            </IndexLink>
          </div>
          <ul className='nav'>
            {this.props.children}
          </ul>
        </div>
      </div>) }
})
