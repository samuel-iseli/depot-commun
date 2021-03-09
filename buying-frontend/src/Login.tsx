import React, { FunctionComponent, useState } from 'react';
import { RouterProps } from 'react-router-dom';
import { Box, Button, FormField, Heading, TextInput } from 'grommet';
import { useAuth } from './context/auth';

const Login : FunctionComponent<RouterProps> = (props) => {
    const auth = useAuth();
    type Creds = {
        email: string,
        password: string
    }

    const [creds, setCreds] = useState<Creds>({email: "", password: ""});

    return (
    <Box>
        <Heading>
            Login
        </Heading>
        <FormField
            label="Email"
        >
            <TextInput
                value={creds.email}
                onChange={(e) => {
                    setCreds((prev_creds) => ({
                        email: e.target.value,
                        password: prev_creds.password
                    }));
                }}
            />
        </FormField>
        <FormField label="Password">
            <TextInput
                type="password"
                value={creds.password}
                onChange={(e) => {
                    setCreds((prev_creds) => ({
                        email: prev_creds.email,
                        password: e.target.value
                    }));
                }}
            />
        </FormField>
        <Box
            margin={{ vertical: 'large' }}
            alignSelf="start"
        >
            <Button
                type="submit"
                label="Login"
                primary
                onClick={() => {
                    auth.login(creds.email, creds.password);
                    props.history.replace('/');
                }}
            />
        </Box>
    </Box>
)};

export default Login;
