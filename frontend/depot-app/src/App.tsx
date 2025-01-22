import { Grommet, Header, Page, PageContent, Text } from 'grommet';

import { ShoppingCart } from './components/ShoppingCart';

const theme = {
  global: {
    font: {
      family: "Roboto",
      size: "18px",
      height: "20px",
    },
  },
};

import { HeaderExtendedProps } from 'grommet';

const AppBar = (props: HeaderExtendedProps) => (
  <Header
    background="brand"
    pad={{ left: "medium", right: "small", vertical: "small" }}
    elevation="medium"
    {...props}
  />
  );


  function App() {
  return (
    <>
    <Grommet theme={theme} full>
      <Page>
        <AppBar >
          <Text size="large">My App</Text>
        </AppBar>
        <PageContent>
            <ShoppingCart />
        </PageContent>
      </Page>
    </Grommet>
    </>
  )
}

export default App
