import { renderToString } from "react-dom/server"
import { createServerRenderer } from "@alexseitsinger/react-ssr"

import { ComposedApp } from "./composed"
import { createStore } from "./store"

export default createServerRenderer(createStore, (req, res, store, history) => {
  const App = ComposedApp({ store, history })
  const html = renderToString(App)
  const state = store.getState()
  res({ html, state })
})
