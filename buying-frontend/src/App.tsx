import React, { useState } from 'react';
import { BrowserRouter as Router, Route, useHistory } from 'react-router-dom';
import { Box, Button, Grommet, Layer, ResponsiveContext } from 'grommet';
import { FormClose } from 'grommet-icons';

import PrivateRoute from './PrivateRoute';
import { ProvideAuth } from './context/auth';

import Header from './Header';
import Menu from './Menu';
import NoLogin from './NoLogin';
import Home from './Home';
import Items from './Items';
import Purchases from './Purchases';


const theme = {
  global: {
    font: {
      family: 'Roboto',
      size: '18px',
      height: '20px',
    },
  },
};

function Main() {
  const [showMenu, setShowMenu] = useState(false);
  const history = useHistory();

  const navigate = (path: string) => {
    history.replace(path);
    setShowMenu(false);
  }

  return (
    <ResponsiveContext.Consumer>
    {size => (
    <Box direction="column" fill>
      <Header showMenu={showMenu} setShowMenu={setShowMenu} />
      <Box align="stretch" justify="start" direction="row" fill>
      {(size !== 'small') ? (
          <Menu navigate={navigate}/>
       ): (
        (showMenu) ? ( 
        <Layer>
          <Box
            background='light-2'
            tag='header'
            justify='end'
            align='center'
            direction='row'
          >
            <Button
              icon={<FormClose />}
              onClick={() => setShowMenu(false)}
            />
          </Box>
          <Box
            fill
            background='light-2'
            align='start'
            justify='start'
            pad='large'
          >
            <Menu navigate={navigate}/>
          </Box>
        </Layer>
        ):( <Box/> ))}
        <Route exact path="/" component={Home} />
        <Route exact path="/nologin" component={NoLogin} />
        <PrivateRoute exact path="/items" component={Items} />
        <PrivateRoute exact path="/purchases" component={Purchases} />
      </Box>
    </Box> )}
  </ResponsiveContext.Consumer>
  );
}

function App() {
  return (
    <ProvideAuth>
      <Router basename='/'>
        <Grommet theme={theme} full>
          <Main/>
        </Grommet>
    </Router>
  </ProvideAuth>
  );
}

export default App;
