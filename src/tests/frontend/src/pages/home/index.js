import React from "react"
import PropTypes from "prop-types"
import { connect } from "react-redux"

function HomePage() {
  return (
    <div>Home Page</div>  
  )
}

HomePage.propTypes = {
  //...
}

const mapState = (state) => ({
  //...
})

const mapDispatch = (dispatch) => ({
  //...
})

export default connect(mapState)(HomePage)
export { HomePage as HomePageNotConnected }
