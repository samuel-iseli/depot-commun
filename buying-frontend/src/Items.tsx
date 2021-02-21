import React, { FunctionComponent } from 'react';
import { RouterProps } from 'react-router-dom';
import { Box, Paragraph } from 'grommet';

type Item = {
  id: string,
  category: string,
  description: string,
  price: number,
};

const TestItems = () => Array.from<Number, Item>( Array(20).keys(), i => ({
    id: '123',
    category: 'Getränke',
    description: 'Bier Paul',
    price: 1.10,
  } ));
  
const Items : FunctionComponent<RouterProps> = (props) => (
    <Box direction="column" justify="start" overflow="scroll" fill="horizontal">
    { TestItems().map(itm => (
      <Box direction="row" border={{"style":"solid"}} 
          pad="medium" gap="medium" flex={false}>
        <Paragraph>{ itm.id }</Paragraph>
        <Box align="start" justify="center" fill="horizontal">
          <Paragraph>
            { itm.description }
          </Paragraph>
        </Box>
        <Paragraph textAlign="end">
          { itm.price }
        </Paragraph>
      </Box>
    ))}
  </Box>
);

export default Items;