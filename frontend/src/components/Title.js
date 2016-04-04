import React from 'react'

var _title = null

export function setTitle (atitle) {
  if (_title) {
    _title.setState({title: atitle})
  }
}

export default React.createClass({
  propTypes: {
    children: React.PropTypes.array
  },

  getInitialState () {
    return {
      title: 'default'
    }
  },

  componentDidMount () {
    _title = this
  },

  render () {
    return (
      <div className='navbar-brand'>{this.state.title}</div>
    ) }
})
