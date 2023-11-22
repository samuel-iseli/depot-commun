import { IonBackButton, IonButtons, IonList, IonContent, IonGrid, IonHeader, IonRow, IonPage, IonTitle, IonToolbar  } from '@ionic/react';
import { useState } from 'react';
import { useRecoilValue, useRecoilState } from 'recoil';
import { cartState, CartDisplayItem } from '../state/Cart';
import  ArticleItem  from '../components/ArticleItem';
import { articlesState, findArticle, ItemCategory } from '../state/Article';


const AddArticleList: React.FC = () => {
    const articles = useRecoilValue(articlesState);

    return (
        <IonPage>
            <IonHeader>
            <IonToolbar>
                <IonButtons slot="start">
                <IonBackButton />
                </IonButtons>
                <IonTitle>Add article</IonTitle>
            </IonToolbar>
            </IonHeader>
                <IonList>
                {articles.map((article) => 
                    (<ArticleItem {...article} />)
                )}
                </IonList>
            <IonContent fullscreen>
            </IonContent>
        </IonPage>);
}

export default AddArticleList;

