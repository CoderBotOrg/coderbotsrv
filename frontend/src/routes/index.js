import React from 'react'
import { Route, IndexRoute } from 'react-router'

// NOTE: here we're making use of the `resolve.root` configuration
// option in webpack, which allows us to specify import paths as if
// they were from the root of the ~/src directory. This makes it
// very easy to navigate to files regardless of how deeply nested
// your current file is.
import CoreLayout from 'layouts/CoreLayout/CoreLayout'
import MainView from 'views/MainView'
import BotView from 'views/BotView'
import ProgramView from 'views/ProgramView'
import LibraryView from 'views/LibraryView'

export default (store) => (
  <Route path='/' component={CoreLayout}>
    <IndexRoute component={MainView}/>
    <Route path='/' component={MainView} title='Home Page'>
      <Route path='/bots' component={BotView} title='Bot List'/>
      <Route path='/programs' component={ProgramView} title='Own Programs'/>
      <Route path='/library' component={LibraryView} title='Public Programs'/>
    </Route>
  </Route>
)
