import { useEffect } from 'react';
import { useNavigate } from 'react-router';
import { useRecoilState, useRecoilValue } from 'recoil';
import { Article } from '../state/Article';
import { activeArticles, activeGroups } from '../state/Article';
import { cartState } from '../state/Cart';
import { showBackButtonState, headerTitleState } from '../state/NavState';
import { ArticleSelector } from '../components/ArticleSelector';

export const AddCartItem = () => {  
    const navigate = useNavigate();
    const articles = useRecoilValue(activeArticles);
    const groups = useRecoilValue(activeGroups);
    const [cart, setCart] = useRecoilState(cartState);
    const [, setShowBackButton] = useRecoilState<boolean>(showBackButtonState);
    const [, setHeaderTitle] = useRecoilState<string>(headerTitleState);

    useEffect(() => {
        setShowBackButton(true);
        setHeaderTitle('Artikel hinzufügen');
        return () => {
            setShowBackButton(false);
        }}, []);

    const articleSelected = (item: Article) => {
        setCart([...cart, item]);
        navigate('/shopping-cart');  
    };

    return (
        <ArticleSelector groups={groups} articles={articles} articleSelected={articleSelected} />
        );
    };

  