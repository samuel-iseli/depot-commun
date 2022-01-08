import { IonButtons, IonContent, IonFab, IonFabButton, IonHeader, IonIcon, IonList, IonMenuButton, IonPage, IonTitle, IonToolbar } from '@ionic/react';
import { CartItem }  from '../components/CartItem';
import { RouteComponentProps } from 'react-router';
import { add } from 'ionicons/icons';
import { useRecoilState, useRecoilValue } from 'recoil';
import { cartState, cartDisplayState } from '../state/Cart';
import { removeItemAtIndex, replaceItemAtIndex } from '../state/Utils';
import React from 'react';
import './Page.css';


const ShoppingCartPage: React.FC<RouteComponentProps> = (props) => {

    const cartDisplay = useRecoilValue(cartDisplayState);
    const [ cart, setCart ] = useRecoilState(cartState);

    const incArticleCount = (code: string) => {
        const idx = cart.findIndex(itm => itm.articleCode == code);
        if (idx !== -1) {
            const item = cart[idx];
            const newCart = replaceItemAtIndex(cart, idx, {
                ...item,
                count: item.count + 1,
            });

            setCart(newCart);
        }
    }

    const decArticleCount = (code: string) => {
        const idx = cart.findIndex(itm => itm.articleCode == code);
        if (idx !== -1) {
            const item = cart[idx];
            const newItem = {
                ...item,
                count: item.count - 1,
            }

            if (newItem.count == 0) {
                setCart(removeItemAtIndex(cart, idx));
            }
            else {
                setCart(replaceItemAtIndex(cart, idx, newItem))
            }
        }
    }

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
            <IonFabButton routerLink="/page/new" >
              <IonIcon icon={add} />
            </IonFabButton>
          </IonFab>
          <IonList>
            {cartDisplay.map((itm) => (
              <CartItem code={itm.code} category={itm.category} description={itm.description} count={itm.count}
                onincrement={() =>incArticleCount(itm.code)} ondecrement={() => decArticleCount(itm.code)} />)
            )}
          </IonList>
        </IonContent>
      </IonPage>
    );
};
  
export default ShoppingCartPage;
