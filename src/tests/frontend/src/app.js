import React from "react"
import { Provider } from "react-redux"
import { Router, Route } from "react-router"

import HomePage from "./pages/home"

export function App({ store, history }) {
  return (
    <Provider store={store}>
      <Router history={history}>
        <Route path={"/"} component={HomePage} exact />
      </Router>
    </Provider>
  )
}
