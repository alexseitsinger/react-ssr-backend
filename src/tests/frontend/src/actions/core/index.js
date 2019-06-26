import { actionTypes } from "./types"

export function setAuthenticated(bool) {
  return {
    type: actionTypes.AUTHENTICATED,
    bool,
  }
}

export function setTokens(obj) {
  return {
    type: actionTypes.TOKENS,
    obj,
  }
}

export function setUser(obj) {
  return {
    type: actionTypes.USER,
    obj,
  }
}

