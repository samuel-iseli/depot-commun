import React, { FunctionComponent, useEffect, useState } from 'react';
import { RouterProps } from 'react-router-dom';
import { Box, Button, Heading } from 'grommet';
import { queryCurrentUser, useAuth } from './context/auth';

const Home : FunctionComponent<RouterProps> = (props) => {
    const auth = useAuth();

    useEffect(() => {
        // query current-user from back-end
        queryCurrentUser()
        .then( userName => {
            console.log('current-user query sucess. user: '+ userName);
            auth.setUserName(userName);
        })
        .catch( error => {
            console.log('error on current-user query: ' + error);
            auth.setUserName('');
        });
    }, [auth.userName]);

    return (
        <Box pad='medium' direction='column'>
            <Heading>This is the Depot Commun App</Heading>

            <Button
                onClick={ () => {
                    props.history.replace('/items');
                }}
                >Artikel-Liste
            </Button>
        </Box>
    );
};

export default Home;