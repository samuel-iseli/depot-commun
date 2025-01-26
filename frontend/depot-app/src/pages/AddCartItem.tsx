import { useEffect } from 'react';
import { useNavigate } from 'react-router';
import { useRecoilState } from 'recoil';
import { Box, List, Text } from 'grommet';
import { ArticleItem } from '../components/ArticleItem';
import { Article, ArticleCategory } from '../state/Article';
import { cartState } from '../state/Cart';
import { NavState, navStateAtom } from '../state/NavState';

const articles: Array<Article> = [
    { code: "123", category: ArticleCategory.Beer, description: "Bier, Paul", price: 1.10},
    { code: "125", category: ArticleCategory.Wine, description: "Ultimo Sogno", price: 1.10},
    ]

export const AddCartItem = () => {  
    const navigate = useNavigate();
    const [cart, setCart] = useRecoilState(cartState);
    const [navState, setNavState] = useRecoilState<NavState>(navStateAtom);

    useEffect(() => {
        console.log('AddCartItem effect: ', cart);
        setNavState({showBackButton: true});
        return () => {
            setNavState({showBackButton: false});
        }}, []);

    const articleClicked = ({ item, index }: { item: Article; index: number }) => {
        setCart([...cart, item]);
        navigate('/shopping-cart');  
    };

    return (
        <Box direction="column" pad="medium" gap="medium">
            <Text size="medium">Artikel auswählen</Text>
            <List data={articles} onClickItem={articleClicked}>
            {(item) => (
                <ArticleItem {...item} />
            )}
            </List>
        </Box>
        );
    };

  