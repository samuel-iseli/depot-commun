import { useEffect } from 'react';
import { useNavigate } from 'react-router';
import { useRecoilState, useRecoilValue } from 'recoil';
import { Box, Tabs, Tab } from 'grommet';
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
    const [showBackButton, setShowBackButton] = useRecoilState<boolean>(showBackButtonState);
    const [headerTitle, setHeaderTitle] = useRecoilState<string>(headerTitleState);

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
        <Tabs>
            <Tab title="Artikel wählen">
                <ArticleSelector groups={groups} articles={articles} articleSelected={articleSelected} />
            </Tab>
        </Tabs>
        );
    };

  