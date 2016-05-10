import React from 'react'
import { Link } from 'react-router'

export default React.createClass({
  propTypes: {
    iconClassName: React.PropTypes.string,
    destLabel: React.PropTypes.string.isRequired
  },

  render () {
    return (
      <li activeClassName='active'>
        <Link {...this.props} title={this.props.destLabel}>
          <i className={this.props.iconClassName}></i>
          <p>{this.props.destLabel}</p>
        </Link>
      </li>
    ) }
})
