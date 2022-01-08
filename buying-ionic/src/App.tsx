import { IonApp, IonRouterOutlet, IonSplitPane } from '@ionic/react';
import { IonReactRouter } from '@ionic/react-router';
import { Redirect, Route } from 'react-router-dom';
import { RecoilRoot } from 'recoil';
import Menu from './components/Menu';
import ShoppingCartPage from './pages/ShoppingCartPage';
import AddArticlePage from './pages/AddArticlePage';

/* Core CSS required for Ionic components to work properly */
import '@ionic/react/css/core.css';

/* Basic CSS for apps built with Ionic */
import '@ionic/react/css/normalize.css';
import '@ionic/react/css/structure.css';
import '@ionic/react/css/typography.css';

/* Optional CSS utils that can be commented out */
import '@ionic/react/css/padding.css';
import '@ionic/react/css/float-elements.css';
import '@ionic/react/css/text-alignment.css';
import '@ionic/react/css/text-transformation.css';
import '@ionic/react/css/flex-utils.css';
import '@ionic/react/css/display.css';

/* Theme variables */
import './theme/variables.css';

const App: React.FC = () => {
  return (
    <IonApp>
      <RecoilRoot>
        <IonReactRouter>
          <IonSplitPane contentId="main">
            <Menu />
            <IonRouterOutlet id="main">
              <Route path="/" exact={true}>
                <Redirect to="/page/Shop" />
              </Route>
              <Route path="/page/Shop" component={ShoppingCartPage} exact={true} />
              <Route path="/page/New" component={AddArticlePage} exact={true} />
              {/* <Route path="/page/:name" exact={true}>
                <Page />
              </Route> */}
            </IonRouterOutlet>
          </IonSplitPane>
        </IonReactRouter>
      </RecoilRoot>
    </IonApp>
  );
};

export default App;
