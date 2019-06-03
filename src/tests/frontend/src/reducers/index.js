import { combineReducers } from "redux"

import { authReducer } from "./auth"
import { homeReducer } from "./home"

export function createRootReducer(history) {
  return combineReducers({
    auth: authReducer,
    home: homeReducer,
  })
}
