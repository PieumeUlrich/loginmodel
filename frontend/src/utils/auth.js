import { AccessibleTwoTone } from '@mui/icons-material'
import {createAuthProvider} from 'react-token-auth'


export const[useAuth, authFetch, login, logout] = 
    createAuthProvider({
        accessTokenKey: 'access_token',
        onUpdatetoken: (token) => fetch('http://localhost:5000/auth/refresh',{
            method: 'POST',
            body: token.refresh_token
        })
        .then(send => send.json())
    });