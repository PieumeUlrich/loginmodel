// import { BehaviorSubject } from 'rxjs';
import getConfig from 'next/config';
import Router from 'next/router';
import { proxy } from 'src/utils/setupProxy';
import { fetchWrapper } from './fetch.service';

const { publicRuntimeConfig } = getConfig();
// const baseUrl = `${publicRuntimeConfig.apiUrl}/users`;
const baseUrl = `${proxy}`;
// const userSubject = new BehaviorSubject(process.browser && JSON.parse(localStorage.getItem('user')));
const userSubject = process.browser && JSON.parse(localStorage.getItem('user'));
const token = process.browser && JSON.parse(localStorage.getItem('token'));

export const userService = {
    // user: userSubject.asObservable(),
    user: userSubject,
    token,
    // get userValue () { return userSubject.value },
    login,
    logout,
    register,
    getAll,
    getById,
    update,
    delete: _delete
};

function login(props) {
    return fetchWrapper.post(`${baseUrl}/auth/login`, props)
}

function logout() {
    // remove user from local storage, publish null to user subscribers and redirect to login page
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    // userSubject.next(null);
    Router.push('/login');
}

function register(user) {
    return fetchWrapper.post(`${baseUrl}/auth/signup `, user);
}

function getAll() {
    try{
        let result = fetchWrapper.get(`${baseUrl}/user/users`);
        console.log(result)
    }
    catch(error){
        console.log(error)
    }
}

function getById(id) {
    try{
        let result = fetchWrapper.get(`${baseUrl}/user/user/${id}`);
        console.log(result)
        }
    catch(error){
        console.log(error)
    }
}

function update(id, params) {
    return fetchWrapper.put(`${baseUrl}/user/user/${id}`, params)
        .then(x => {
            // update stored user if the logged in user updated their own record
            if (id === userSubject.value.id) {
                // update local storage
                const user = { ...userSubject.value, ...params };
                localStorage.setItem('user', JSON.stringify(user));

                // publish updated user to subscribers
                userSubject.next(user);
            }
            return x;
        });
}

// prefixed with underscored because delete is a reserved word in javascript
function _delete(id) {
    return fetchWrapper.delete(`${baseUrl}/${id}`);
}