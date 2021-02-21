import React, { FunctionComponent } from 'react';
import { RouterProps } from 'react-router-dom';
import { Box, Button, Heading } from 'grommet';

const Home : FunctionComponent<RouterProps> = (props) => (
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

export default Home;