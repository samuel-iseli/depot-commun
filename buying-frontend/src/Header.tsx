import React, { FunctionComponent, SetStateAction, Dispatch, useState } from 'react';
import { Box, Button, ResponsiveContext } from 'grommet';
import { Menu, Login, Logout, StatusGoodSmall  } from 'grommet-icons';
import { useAuth} from './context/auth';

interface HeaderProps {
  showMenu: boolean;
  setShowMenu: Dispatch<SetStateAction<boolean>>;
}

const Header : FunctionComponent<HeaderProps> = (props) => {
  const auth = useAuth();

  return (
  <ResponsiveContext.Consumer> 
    { size => (
    <Box
      tag='header'
      direction='row'
      align='start'
      justify='start'
      background='brand'
      pad={{ left: 'medium', right: 'small', vertical: 'small' }}
      elevation='medium'
      style={{ zIndex: 1 }}
    >
      {(size == 'small') && (
        <Box align='start' justify="start">
          <Button
            onClick={() => {
              props.setShowMenu(!props.showMenu);
            }}
            focusIndicator={false}>
            <Menu />
          </Button>
        </Box> )}
      <Box fill align='center'>Depot Commun</Box> 
      <Box>{ auth.userName }</Box>
      <Box pad={{left: 'small', right: 'small'}}>
        {auth.isAuthenticated ? (
          <Button
            onClick={() => auth.logout()}>
            <Logout/>
          </Button> ) : (
          <Button href= { auth.loginUrl }><Login/></Button> )
        }
      </Box>
    </Box> 
    )}
  </ResponsiveContext.Consumer>
  )};
  
export default Header;
