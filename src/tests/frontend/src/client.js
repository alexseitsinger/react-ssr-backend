import ReactDOM from "react-dom"
import { createClientRenderer } from "@alexseitsinger/react-ssr"

import { createStore } from "./store"

export const store = createClientRenderer(createStore, (store, history) => {
  const App = ComposedApp({ store, history })
  const mountPoint = document.getElementsByTagName("main")[0]
  ReactDOM.hydrate(App, mountPoint)
})
