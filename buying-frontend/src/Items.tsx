import React, { FunctionComponent, useState, useEffect } from 'react';
import { RouterProps } from 'react-router-dom';
import { Box, Paragraph } from 'grommet';
import axios from 'axios';

type Item = {
  product_nr: string,
  tags: string,
  name: string,
  price: number,
};

const Items : FunctionComponent<RouterProps> = (props) => {

  const [list, setList ] = useState<Item []>([]);

  useEffect(() => {
    // called when component has mounted

    // load items list
    axios.get('/buying/items/available-items/')
    .then(response => {
      setList(response.data);
    })
    .catch(error => {
      console.log('error on getting items: ' + error)
    })
  }, [])

  return (
    <Box direction="column" justify="start" overflow="scroll" fill="horizontal">
    { list.map(itm => (
      <Box direction="row" border={{"style":"solid"}} 
          pad="medium" gap="medium" flex={false}>
        <Paragraph>{ itm.product_nr }</Paragraph>
        <Box align="start" justify="center" fill="horizontal">
          <Paragraph>
            { itm.name }
          </Paragraph>
        </Box>
        <Paragraph textAlign="end">
          { itm.price }
        </Paragraph>
      </Box>
    ))}
  </Box>
)};

export default Items;