import { Grommet, Page, PageContent } from 'grommet';
import { Routes, Route } from 'react-router';
import { AppBar } from './AppBar';
import { ShoppingCart } from './pages/ShoppingCart';
import { AddCartItem } from './pages/AddCartItem';
import { Home } from './pages/Home';


const theme = {
  global: {
    font: {
      family: "Roboto",
      size: "18px",
      height: "20px",
    },
  },
};



  function App() {
    return (
      <>
      <Grommet theme={theme} full>
        <Page>
          <AppBar />
          <PageContent>
            <Routes>
              <Route path="/" Component={Home} />
              <Route path="/shopping-cart"  element={<ShoppingCart />} /> 
              <Route path="/add-cart-item" element={<AddCartItem />} />
            </Routes>
          </PageContent>
        </Page>
      </Grommet>
      </>
    )
}

export default App
