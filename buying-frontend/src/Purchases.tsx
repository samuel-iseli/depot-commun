import React, { FunctionComponent } from 'react';
import { RouterProps } from 'react-router-dom';
import { Box, Heading } from 'grommet';

const Purchases : FunctionComponent<RouterProps> = (props) => (
    <Box pad='large'>
        <Heading>This is the Purchases List</Heading>

    </Box>
);

export default Purchases;