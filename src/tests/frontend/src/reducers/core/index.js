import initialState from "./state.json"
import { actionTypes } from "actions/core/types"


export function authReducer(state = initialState, action) {
  switch (action.type) {
    default: {
      return state
    }
    case actionTypes.AUTHENTICATED:
    case actionTypes.TOKENS:
    case actionTypes.USER: {
      return authenticationReducer(state.authentication, action)
    }
  }
}
