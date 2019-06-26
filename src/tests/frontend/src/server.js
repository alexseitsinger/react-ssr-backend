import { renderToString } from "react-dom/server"
import { createServerRenderer } from "@alexseitsinger/react-ssr"

import { composed } from "./composed"
import { createStore } from "./store"

export default createServerRenderer({
  createStore,
  render: (req, res, store, history) => {
    const App = composed({ store, history })
    const html = renderToString(App)
    const state = store.getState()
    res({ html, state })
  },
})
