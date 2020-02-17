import React from "react"
import PropTypes from "prop-types"
import { connect } from "react-redux"

function HomePage({ isAuthenticated, }) {
  return (
    <div>Home Page</div>
  )
}

HomePage.propTypes = {
  isAuthenticated: PropTypes.bool.isRequired,
}

const mapState = state => ({
  isAuthenticated: state.core.authentication.isAuthenticated,
})

const mapDispatch = dispatch => ({
  //....
})

export default connect(mapState, mapDispatch)(HomePage)
export { HomePage as HomePageNotConnected }
