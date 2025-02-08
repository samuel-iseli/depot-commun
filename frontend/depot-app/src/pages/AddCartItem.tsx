import { useEffect } from 'react';
import { useNavigate } from 'react-router';
import { useRecoilState, useRecoilValue } from 'recoil';
import { Box, List, Tabs, Tab, Text } from 'grommet';
import { ArticleItem } from '../components/ArticleItem';
import { Article } from '../state/Article';
import { activeArticles } from '../state/Article';
import { cartState } from '../state/Cart';
import { showBackButtonState, headerTitleState } from '../state/NavState';
import { QrScannerComponent } from '../components/QrScannerComponent';

export const AddCartItem = () => {  
    const navigate = useNavigate();
    const articles = useRecoilValue(activeArticles);
    const [cart, setCart] = useRecoilState(cartState);
    const [showBackButton, setShowBackButton] = useRecoilState<boolean>(showBackButtonState);
    const [headerTitle, setHeaderTitle] = useRecoilState<string>(headerTitleState);

    useEffect(() => {
        setShowBackButton(true);
        setHeaderTitle('Artikel hinzufügen');
        return () => {
            setShowBackButton(false);
        }}, []);

    const articleClicked = ({ item, index }: { item: Article; index: number }) => {
        setCart([...cart, item]);
        navigate('/shopping-cart');  
    };

    return (
        <Tabs>
            <Tab title="QR-Code">
                <Box pad="medium" gap="xlarge" justify="between" fill="vertical" direction="column">
                    <QrScannerComponent />
                </Box>
            </Tab>
            <Tab title="Artikel wählen">
                <List data={articles} onClickItem={articleClicked} defaultItemProps={{ pad: 'none'}}>
                {(item) => (
                    <ArticleItem {...item} />
                )}
                </List>
            </Tab>
        </Tabs>
        );
    };

  