import { useState } from 'react'
import proxy from './setupProxy'

export default function useToken (){
    const getToken = async () => {
        const tokenString = process.browser && localStorage.getItem('token')
        const userToken = JSON.parse(tokenString)
        return userToken
    };

    const [token, setToken] = useState(getToken())

    const saveToken = (userToken) => {
        localStorage.setItem('token', JSON.stringify(userToken))
        setToken(userToken);
    };

    const updateToken = (refreshToken) => {
        fetch(`${proxy}/auth/refresh`,{
            method: 'POST',
            body: JSON.stringify(refreshToken)
        })
        .then(send => send.json())
        .then(res => {
            saveToken(res.access_token)
        })
    }
    return {
        setToken: saveToken,
        token
    }
}