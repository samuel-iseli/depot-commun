import { useNavigate } from 'react-router';
import { Box, Button, List, Text } from 'grommet';
import { Add, Checkmark } from 'grommet-icons';
import { useRecoilState } from 'recoil';
import { cartState } from '../state/Cart';
import ArticleItem from '../components/ArticleItem';


const floatingActionBarStyle: React.CSSProperties = {
  position: 'fixed',
  bottom: '20px',
  left:'0', 
  right:'0', 
  margin: 'auto', 
  width: 'fit-content'
};

export const ShoppingCart = () => {
  const navigate = useNavigate();
  const [cartItems, setCartItems] = useRecoilState(cartState);

  const removeItem = (index: number) => {
    const newCartItems = cartItems.slice();
    newCartItems.splice(index, 1)
    setCartItems(newCartItems);
  }

  return (
    <>
      <List data={cartItems} defaultItemProps={{ pad: 'none'}} >
          {(item, index) => (
              <ArticleItem {...item} onRemove={() => removeItem(index)} />
          )}
      </List>
      <Box direction="row" style={floatingActionBarStyle} >
        <Button icon={<Add/>} primary onClick={() => navigate('/add-cart-item')} />
        <Button icon={<Checkmark/>} secondary />
      </Box>
    </>
    );
};