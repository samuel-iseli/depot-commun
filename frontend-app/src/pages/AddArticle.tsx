import { IonBackButton, IonButtons, IonCol, IonContent, IonGrid, IonHeader, IonRow, IonPage, IonTitle, IonToolbar  } from '@ionic/react';
import { useState } from 'react';
import { useRecoilValue, useRecoilState } from 'recoil';
import { cartState, CartDisplayItem } from '../state/Cart';
import { CartItem } from '../components/CartItem';
import NumKeyboard from '../components/NumKeyboard';
import { articlesState, findArticle, ItemCategory } from '../state/Article';

const AddArticle: React.FC = () => {
    const articles = useRecoilValue(articlesState);
    const [cart, setCart] = useRecoilState(cartState);
    const [articleNum, setArticleNum] = useState("");
    const [articleFound, setArticleFound] = useState(false);
    const [tempCartItem, setTempCartItem] = useState<CartDisplayItem>();

    const handleKey = (arg: string) => {
      console.debug("pressed key " + arg);

      // OK key
      if (arg === "OK") {
        // add article to shopping cart
        if (tempCartItem) {
          const article = findArticle(tempCartItem.code , articles);
          if (article) {
            console.debug("add to cart");
            setCart((cart) => [ ...cart,
              {
                articleCode: articleNum,
                count: tempCartItem.count,
              }
            ]);

            // clear temp cart item
            setTempCartItem(undefined);
            setArticleNum("");
            setArticleFound(false);
          }
        }
        return;
      }

      let newArticleNum = articleNum;
      if (arg === "Back") {
        if (articleNum.length > 0) {
          newArticleNum = articleNum.substring(0, articleNum.length-1);
        }
      } else {
        if (articleNum.length < 3) {
          newArticleNum = articleNum + arg;
        }
      }
      setArticleNum(newArticleNum);

      if (newArticleNum.length === 3) {
          // 3 digits entered
          const article = findArticle(newArticleNum, articles);
          if (article) {
              setArticleFound(true);
              setTempCartItem({
                code: article.code,
                description: article.description,
                category: article.category,
                price: article.price,
                count: 1,
                itemprice: article.price,
              });
          }
          else {
              setTempCartItem({
                code: "",
                description: "unknown Article",
                category: ItemCategory.Open,
                price: 0,
                count: 0,
                itemprice: 0,
              });
          }
      } else {
        setTempCartItem(undefined);
        setArticleFound(false);
      }
    };

    const incCount = () => {
      if (tempCartItem) {
        setTempCartItem({
          ...tempCartItem,
          count: tempCartItem.count + 1,
        });
      }
    };

    const decCount = () => {
      if (tempCartItem && tempCartItem.count > 0) {
        setTempCartItem({
          ...tempCartItem,
          count: tempCartItem.count -1,
        });
      }
    };

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

        <IonContent fullscreen>
        <IonHeader collapse="condense">
            <IonToolbar>
            <IonTitle size="large">New</IonTitle>
            </IonToolbar>
        </IonHeader>
        <NumKeyboard callback={handleKey} okEnabled={articleFound} />
        <IonGrid>
            <IonRow>
              <IonCol size="4"></IonCol>
              <IonCol class="ion-justify-content-center">
                  {articleNum}
              </IonCol>
              <IonCol size="4"></IonCol>
            </IonRow>
            <IonRow>
                <IonCol> {
                    (tempCartItem && (                      
                  <CartItem 
                    code={tempCartItem.code} description={tempCartItem.description} 
                    category={tempCartItem.category} count={tempCartItem.count} 
                    onincrement={incCount} ondecrement={decCount}
                  />))
                }  
                </IonCol> 
            </IonRow>
        </IonGrid>
        </IonContent>
    </IonPage>
    );
};

export default AddArticle;
