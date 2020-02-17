import { 
  createStore as createReduxStore,
  compose,
  applyMiddleware,
} from "redux"

import { createRootReducer } from "./reducers"

export function createStore(history, initialState = {}){
  const rootReducer = createRootReducer(history)
  const middleware = []
  const storeEnhancers = compose(applyMiddleware(...middleware))
  const store = createReduxStore(rootReducer, initialState, storeEnhancers)
  return store
}
