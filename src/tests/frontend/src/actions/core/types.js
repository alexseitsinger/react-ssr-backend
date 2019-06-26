import { createActionTypes } from "@alexseitsinger/redux-action-types"

export const actionTypes = createActionTypes("core", [
  "authenticated",
  "user",
  "tokens",
  ["get", [
    ["tokens", [
      "success",
      "failure",
    ]],
    ["user", [
      "success",
      "failure",
    ]],
  ]]
])


