import { combineReducers } from "redux"

import { coreReducer } from "./core"
import { homeReducer } from "./home"

export function createRootReducer(history) {
  return combineReducers({
    core: coreReducer,
    home: homeReducer,
  })
}
