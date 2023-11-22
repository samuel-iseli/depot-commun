import { Redirect, Route } from 'react-router-dom';
import { IonApp, IonRouterOutlet, setupIonicReact } from '@ionic/react';
import { IonReactRouter } from '@ionic/react-router';
import { RecoilRoot } from 'recoil';
import Home from './pages/Home';
import ShoppingCart from './pages/ShoppingCart';
import AddArticleKeys from './pages/AddArticleKeys';
import AddArticleList from './pages/AddArticleList';

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

setupIonicReact();

const App: React.FC = () => (
  <IonApp>
    <RecoilRoot>
      <IonReactRouter>
        <IonRouterOutlet>
          <Route exact path="/cart">
            <ShoppingCart />
          </Route>
          <Route exact path="/new_keys" component={AddArticleKeys} />
          <Route exact path="/new_list" component={AddArticleList} />
          <Route exact path="/">
            <Redirect to="/cart" />
          </Route>
        </IonRouterOutlet>
      </IonReactRouter>
    </RecoilRoot>
  </IonApp>
);

export default App;
