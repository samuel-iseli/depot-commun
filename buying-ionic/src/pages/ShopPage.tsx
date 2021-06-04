import { IonButtons, IonContent, IonFab, IonFabButton, IonHeader, IonIcon, IonItem, IonList, IonMenuButton, IonPage, IonTitle, IonToolbar } from '@ionic/react';
import { ShopItem, ItemCategory }  from '../components/ShopItem';
import { useParams } from 'react-router';
import { add } from 'ionicons/icons';
import './Page.css';


const ShopPage: React.FC = () => {

    const { name } = useParams<{ name: string; }>();

    return (
      <IonPage>
        <IonHeader>
          <IonToolbar>
            <IonButtons slot="start">
              <IonMenuButton />
            </IonButtons>
            <IonTitle>Shop</IonTitle>
          </IonToolbar>
        </IonHeader>
  
        <IonContent fullscreen>
          <IonHeader collapse="condense">
            <IonToolbar>
              <IonTitle size="large">Shop</IonTitle>
            </IonToolbar>
          </IonHeader>
          <IonFab vertical="bottom" horizontal="center">
            <IonFabButton>
              <IonIcon icon={add} />
            </IonFabButton>
          </IonFab>
          <IonList>
              <ShopItem category={ItemCategory.Beer}  description="Bier, Paul" count={1} />
              <ShopItem category={ItemCategory.Beer} description="Bier, Sprint" count={3} />
              <ShopItem category={ItemCategory.Wine} description="Prosecco, Volpi" count={1} />
          </IonList>
        </IonContent>
      </IonPage>
    );
  };
  
  export default ShopPage;
  