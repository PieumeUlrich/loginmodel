import { Link } from 'next/link'
import { useRouter } from 'next/router'
import { useState, useEffect } from 'react'
import Dashboard from './dashboard'
import Login from './login'
// import authCheck from './../services/auth.service'

const IndexPage = () => {
  const user = process.browser && JSON.parse(localStorage.getItem('user'))
    if(user)
        return <Dashboard />
    return (
        <Login />
    )
}

export default IndexPage