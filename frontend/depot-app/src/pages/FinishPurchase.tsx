import { useRecoilValue, useRecoilState } from "recoil";
import { Accordion, AccordionPanel, Box, Button, List, Notification, Text } from "grommet";
import { ArticleItem } from "../components/ArticleItem";
import { cartState } from "../state/Cart";
import { Article } from "../state/Article";
import { useState, useEffect } from "react";
import { headerTitleState, showBackButtonState } from "../state/NavState";
import { useNavigate } from "react-router";

export const FinishPurchase = () => {
    const [showBackButton, setShowBackButton] = useRecoilState(showBackButtonState);
    const [headerTitle, setHeaderTitle] = useRecoilState<string>(headerTitleState);
    const cartItems = useRecoilValue(cartState);
    const itemCount = cartItems.length;
    const priceSum = cartItems.reduce<number>((sum: number, item: Article) => sum + Number(item.price), 0);
    const navigate = useNavigate();
    const [notificationVisible, setNotificationVisible] = useState(false);
    const [cart, setCart] = useRecoilState(cartState);

    useEffect(() => {
        setShowBackButton(true);
        setHeaderTitle('Einkauf abschliessen');
        return () => {
            setShowBackButton(false);
        }}, []);
        
    const finishPurchase = () => {
        setCart([]);
        setNotificationVisible(true);
    };

    return (
        <Box pad="medium" gap="xlarge" justify="between" fill="vertical" direction="column">
            <Text>Einkauf abschliessen.</Text>

            <Accordion>
                <AccordionPanel label={`${itemCount} Artikel`}>
                    <List data={cartItems} defaultItemProps={{ pad: 'none'}} >
                        {(item, index) => (
                        <ArticleItem {...item} />
                        )}
                    </List>
                </AccordionPanel>
            </Accordion>

            <Box direction="row" justify="between">
                <Text>Gesamtpreis</Text>
                <Text alignSelf="end" textAlign="end" >{`${priceSum.toFixed(2)}`}</Text>
            </Box>

            <Box direction="column">
                <Button primary label="Bestätigen" disabled={notificationVisible} onClick={finishPurchase}  />
            </Box>
            {notificationVisible && (
            <Notification
                toast={{ position: 'bottom-right' }}
                status="info"
                title="Einkauf bestätigt"
                message="Vielen Dank für deinen Besuch im Depot-Commün"
                onClose={() => {navigate('/');}}
            />
    )}

        </Box>
    );
};
