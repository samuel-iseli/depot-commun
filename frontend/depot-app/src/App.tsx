import { useState } from 'react'
import viteLogo from '/vite.svg'
import { Grommet, Header, Page, PageContent, PageHeader, Text } from 'grommet';

const theme = {
  global: {
    font: {
      family: "Roboto",
      size: "18px",
      height: "20px",
    },
  },
};

const AppBar = (props) => (
  <Header
    background="brand"
    pad={{ left: "medium", right: "small", vertical: "small" }}
    elevation="medium"
    {...props}
  />
  );


  function App() {
  const [count, setCount] = useState(0)

  return (
    <>
    <Grommet theme={theme} full>
      <Page>
        <AppBar>
          <Text size="large">My App</Text>
        </AppBar>
        <PageContent>
          <PageHeader title="Page Header"/>
          <div className="card">
            <button onClick={() => setCount((count) => count + 1)}>
              count is {count}
            </button>
            <p>
              Edit <code>src/App.tsx</code> and save to test HMR
            </p>
          </div>
          <p className="read-the-docs">
            Click on the Vite and React logos to learn more
          </p>
        </PageContent>
      </Page>
    </Grommet>
    </>
  )
}

export default App
