import { IonButtons, IonContent, IonFab, IonFabButton, IonFabList, IonHeader, IonIcon, IonList, IonMenuButton, IonPage, IonTitle, IonToolbar } from '@ionic/react';
import { CartItem }  from '../components/CartItem';
import { RouteComponentProps } from 'react-router';
import { add, keypad, list } from 'ionicons/icons';
import { useRecoilState, useRecoilValue } from 'recoil';
import { cartState, cartDisplayState } from '../state/Cart';
import { removeItemAtIndex, replaceItemAtIndex } from '../state/Utils';
import React from 'react';


const ShoppingCart: React.FC = () => {

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
            <IonFabButton >
              <IonIcon icon={add} />
            </IonFabButton>
            <IonFabList side="end">
              <IonFabButton routerLink="/new_list" >
                <IonIcon icon={list} />
              </IonFabButton>
              <IonFabButton routerLink="/new_keys" >
                <IonIcon icon={keypad} />
              </IonFabButton>
            </IonFabList>
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
  
export default ShoppingCart;
