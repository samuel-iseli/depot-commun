import { useEffect } from 'react';
import { useNavigate } from 'react-router';
import { useRecoilState, useRecoilValue } from 'recoil';
import { Box, List, Text } from 'grommet';
import { ArticleItem } from '../components/ArticleItem';
import { Article } from '../state/Article';
import { activeArticles } from '../state/Article';
import { cartState } from '../state/Cart';
import { NavState, navStateAtom } from '../state/NavState';

export const AddCartItem = () => {  
    const navigate = useNavigate();
    const articles = useRecoilValue(activeArticles);
    const [cart, setCart] = useRecoilState(cartState);
    const [navState, setNavState] = useRecoilState<NavState>(navStateAtom);

    useEffect(() => {
        setNavState({showBackButton: true});
        return () => {
            setNavState({showBackButton: false});
        }}, []);

    const articleClicked = ({ item, index }: { item: Article; index: number }) => {
        setCart([...cart, item]);
        navigate('/shopping-cart');  
    };

    return (
        <>
            <List data={articles} onClickItem={articleClicked} defaultItemProps={{ pad: 'none'}}>
            {(item) => (
                <ArticleItem {...item} />
            )}
            </List>
        </>
        );
    };

  