import React, {FunctionComponent } from 'react';
import { Redirect, Route, RouteProps, RouteComponentProps } from 'react-router-dom';
import { useAuth } from "./context/auth";

const PrivateRoute: FunctionComponent<RouteProps> = (props) => {
    const auth = useAuth();
    const {children, component: Component, ...rest} = props;

    return(
        <Route {...rest} render={(renderProps) => 
            auth.isAuthenticated ? (
                Component ? (
                <Component {...renderProps} />
                ) : (
                children    
                )
            ) : (
            <Redirect to="/nologin"/>
        )}
        />
    );
}

export default PrivateRoute;