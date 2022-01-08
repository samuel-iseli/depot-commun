import {
  IonContent,
  IonIcon,
  IonItem,
  IonLabel,
  IonList,
  IonListHeader,
  IonMenu,
  IonMenuToggle,
  IonNote,
} from '@ionic/react';

import { useLocation } from 'react-router-dom';
import {bagCheckOutline, bagCheckSharp, cartOutline, cartSharp, logOutOutline, settingsOutline, settingsSharp } from 'ionicons/icons';
import './Menu.css';

interface AppPage {
  url: string;
  iosIcon: string;
  mdIcon: string;
  title: string;
}

const appPages: AppPage[] = [
  {
    title: 'Shop',
    url: '/page/Shop',
    iosIcon: cartOutline,
    mdIcon: cartSharp
  },
  {
    title: 'Purchases',
    url: '/page/Purchases',
    iosIcon: bagCheckOutline,
    mdIcon: bagCheckSharp
  },
  {
    title: 'Settings',
    url: '/page/Settings',
    iosIcon: settingsOutline,
    mdIcon: settingsSharp
  },
];

const labels = ['Family', 'Friends', 'Notes', 'Work', 'Travel', 'Reminders'];

const Menu: React.FC = () => {
  const location = useLocation();

  return (
    <IonMenu contentId="main" type="overlay">
      <IonContent>
        <IonList id="main-menu-list">
          <IonListHeader>Depot Comün</IonListHeader>
          <IonNote>user@login.com</IonNote>
          {appPages.map((appPage, index) => {
            return (
              <IonMenuToggle key={index} autoHide={false}>
                <IonItem className={location.pathname === appPage.url ? 'selected' : ''} routerLink={appPage.url} routerDirection="none" lines="none" detail={false}>
                  <IonIcon slot="start" ios={appPage.iosIcon} md={appPage.mdIcon} />
                  <IonLabel>{appPage.title}</IonLabel>
                </IonItem>
              </IonMenuToggle>
            );
          })}
        </IonList>

        <IonList id="login-menu-list">
          <IonItem lines="none" >
            <IonIcon slot="start" icon={logOutOutline} />
            <IonLabel>Logout</IonLabel>
          </IonItem>
        </IonList>
      </IonContent>
    </IonMenu>
  );
};

export default Menu;
