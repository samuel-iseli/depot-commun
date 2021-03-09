import React, { createContext, FunctionComponent, useContext, useState } from 'react';
import axios from 'axios';

// set django testserver address in development mode
if (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
    axios.defaults.baseURL = 'http://localhost:8000';
}

type Auth = {
    isAuthenticated: boolean,
    userName: string,
    authToken: string,
    login: (userName: string, password: string) => boolean,
    logout: () => void
}

const dummyLogin = (userName: string, password: string) => false;
const authContext = createContext<Auth>({
    isAuthenticated: false, 
    userName: '', authToken: '',
    login: dummyLogin,
    logout: () => {}
});

// Provider component
// makes auth object available to any child component that calls useAuth().
export const ProvideAuth: FunctionComponent = (props) => {
    const auth = useProvideAuth();
    return <authContext.Provider value={auth}>{props.children}</authContext.Provider>;
}

export function useAuth() {
    return useContext(authContext);
}

function useProvideAuth(): Auth
{
    const [token, setToken] = useState<string>('');
    const [user, setUser] = useState<string>('');

    const login = (userName: string, password: string) => {
        // perform login and set token
        const cred = {username: userName, password: password};
        axios
            .post("/buying/api-token-auth/", cred)
            .then(response => {
                const { token } = response.data;
                console.log('api-token-auth call successful.')
                axios.defaults.headers.common["Authorization"] = "Token " + token;
                setToken(token);
                setUser(userName);
                return true;
            })
            .catch(error => {
                console.log(error)
                return false;
            });

        return false;
    }

    const logout = () => {
        setToken('');
        setUser('');
    }
    
    return {
        isAuthenticated: token !== '',
        userName: user,
        authToken: token,
        login,
        logout
    }
}
