import React, { FunctionComponent } from 'react';
import { RouterProps } from 'react-router-dom';
import { Box, Button, FormField, Heading, TextInput } from 'grommet';


const Login : FunctionComponent<RouterProps> = (props) => (
    <Box>
        <Heading>
            Login
        </Heading>
        <FormField
            label="Email"
        >
            <TextInput
            />
        </FormField>
        <FormField label="Password">
            <TextInput
                type="password"
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
                    props.history.replace('/');
                }}
            />
        </Box>
    </Box>
);

export default Login;
