import React, {FunctionComponent} from 'react';
import {Box, Button, Nav} from 'grommet'
import {
    Home, Vend, Basket, Money, Performance  
  } from 'grommet-icons';

type MenuProps = { navigate : (path: string) => void };

const Menu : FunctionComponent<MenuProps> = (props) => (
    <Box align="start" justify="start" direction="column" 
        background={{"color":"background-back","dark":false,"opacity":"medium"}} 
        pad="small" 
        basis="small" 
        gap="large">
      <Nav align="start" flex={false} pad="small" gap="large">
        <Button label="Home" icon={<Home />} plain 
            onClick={()=> props.navigate('/')}/>
        <Button label="Articles" icon={<Vend />} plain
            onClick={()=> props.navigate('/items')}/>
        <Button label="Purchases" icon={<Basket />} plain
            onClick={()=> props.navigate('/purchases')} />
        <Button label="Invoices" icon={<Money />} plain />
      </Nav>
      <Nav align="start" flex={false} pad="small">
        <Button label="Settings" icon={<Performance />} plain />
      </Nav>
    </Box>
  );

export default Menu;
