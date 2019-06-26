import { hydrate } from "react-dom"
import { createClientRenderer } from "@alexseitsinger/react-ssr"

import { createStore } from "./store"
import { composed } from "./composed"

export const store = createClientRenderer({
  createStore,
  render: (store, history) => {
    const App = composed({ store, history })
    const mountPoint = document.getElementsByTagName("main")[0]
    hydrate(App, mountPoint)
  },
})
