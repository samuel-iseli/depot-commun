import { IonButton, IonIcon, IonItem, IonLabel, IonNote } from '@ionic/react';
import { basketOutline, beerOutline, wineOutline } from 'ionicons/icons';
import { add, remove } from 'ionicons/icons';

export enum ItemCategory {
    Beer,
    Wine,
    Beverage,
    Packaged,
    Open,
    Household
}

interface ShopItemProps {
    category: ItemCategory;
    description: string;
    count: number;
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

export const ShopItem: React.FC<ShopItemProps> = (props) => {
    return (
        <IonItem>
            <IonItem>
                <IonIcon icon={iconFromCategory(props.category)} />
            </IonItem>
            <IonLabel>{props.description}</IonLabel>
            <IonItem slot="end">
                <IonButton size="small" color="light">
                    <IonIcon icon={remove} />
                </IonButton>
                <IonLabel>{props.count}</IonLabel>
                <IonButton size="small" color="light">
                    <IonIcon icon={add} />
                </IonButton>
            </IonItem>
        </IonItem>
    );
};