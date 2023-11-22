import { IonButton, IonGrid, IonRow, IonCol, IonIcon, IonItem, IonLabel } from '@ionic/react';
import { Article } from '../state/Article';

const ArticleItem: React.FC<Article> = (props) => {
    return (
        <IonItem>
            {props.description}
            {props.price}
        </IonItem>
    );
};

export default ArticleItem;
