import { IonButton, IonGrid, IonRow, IonCol, IonIcon, IonItem, IonLabel } from '@ionic/react';
import { basketOutline, beerOutline, wineOutline } from 'ionicons/icons';
import { add, remove } from 'ionicons/icons';
import { ItemCategory } from '../state/Article';

interface CartItemProps {
    code: string;
    category: ItemCategory;
    description: string;
    count: number;
    onincrement: () => void;
    ondecrement: () => void;
  }
  
const iconFromCategory = (cat : ItemCategory) => {
    if (cat == ItemCategory.Beer) {
        return beerOutline;
    } 
    if (cat == ItemCategory.Wine) {
        return wineOutline;
    }
    else
        return basketOutline;
};

const CartItemGrid: React.FC<CartItemProps> = (props) => {
    return (
        <IonItem>
            <IonGrid>
                <IonRow>
                    <IonCol size="2">
                        <IonIcon icon={iconFromCategory(props.category)} />
                    </IonCol>
                    <IonCol>
                        <IonLabel>{props.description}</IonLabel>
                    </IonCol>
                    <IonCol size="6">
                        <IonButton size="small" fill="clear" onClick={props.ondecrement}>
                            <IonIcon icon={remove} />
                        </IonButton>
                        <IonLabel>{props.count}</IonLabel>
                        <IonButton size="small" fill="clear" onClick={props.onincrement}>
                            <IonIcon icon={add} />
                        </IonButton>
                    </IonCol>
                </IonRow>
            </IonGrid>
        </IonItem>
    );
};

const CartItemItem: React.FC<CartItemProps> = (props) => {
    return (
        <IonItem>
            <IonItem item-left >
                <IonIcon icon={iconFromCategory(props.category)} />
            </IonItem>
            <IonLabel>{props.description}</IonLabel>
            {/* <IonItem item-right> */}
                <IonButton size="small" fill="clear" onClick={props.ondecrement} item-right>
                    <IonIcon icon={remove} />
                </IonButton>
               {props.count}
                <IonButton size="small" fill="clear" onClick={props.onincrement} item-right>
                    <IonIcon icon={add} />
                </IonButton>
            {/* </IonItem> */}
        </IonItem>
    );
};

export const CartItem = CartItemItem; 
