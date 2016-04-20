/* @flow */
import React, { PropTypes } from 'react'
import Program from '../components/Program'
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
    status: PropTypes.number.isRequired,
    children: PropTypes.array
  },
  getInitialState () {
    return {
      programs: [],
      tags: []
    }
  },

  componentDidMount () {
    console.log(this.props)
    console.log('status: ' + this.props.status + ' tags: ' + this.state.tags)
    CoderBotSrv.findPrograms(this.props.status).then(function (program_list) {
      console.log(program_list)
      this.setState({
        programs: program_list
      })
    }.bind(this), 'json')
  },

  handleTags: function (e) {
    console.log('tags: ' + e.target.value)
    this.setState({
      tags: e.target.value.split(', ')
    })
  },

  render () {
    return (
      <div className='content'>
        <div className='container-fluid'>
          <input type='text' name='tags' placeholder='tags, ...' onChange={this.handleTags}/>
          <div className='row'>
            {this.state.programs.map(function (program) {
              return (
                <Program key={program.uid}
                  programName={program.name}
                  programId={program.uid}
                  programImage='/static/img/coderbot_logo_128.png'/>)
            })
          }
          </div>
        </div>
      </div>
    )
  }
})
