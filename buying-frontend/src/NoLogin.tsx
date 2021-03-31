import React, { FunctionComponent } from 'react';
import { RouterProps } from 'react-router-dom';
import { Box, Heading, Paragraph } from 'grommet';
import { useAuth } from './context/auth';

const NoLogin : FunctionComponent<RouterProps> = (props) => {
    const auth = useAuth();

    return (
    <Box>
        <Heading>
            No Login
        </Heading>
        <Paragraph>
            Your are not logged in.
            Please <a href={ auth.loginUrl }> log in</a>.
        </Paragraph>
    </Box>
)};

export default NoLogin;
