import React, { FunctionComponent, SetStateAction, Dispatch } from 'react';
import { Box, Button, ResponsiveContext } from 'grommet';
import { Menu  } from 'grommet-icons';

interface HeaderProps {
  showMenu: boolean;
  setShowMenu: Dispatch<SetStateAction<boolean>>;
}

const Header : FunctionComponent<HeaderProps> = (props) => (
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
          focusIndicator={false}
        ><Menu /></Button>
      </Box> )}
      <Box fill align='center'>Depot Commun</Box> 
    </Box> 
    )}
  </ResponsiveContext.Consumer>
  );
  
export default Header;
