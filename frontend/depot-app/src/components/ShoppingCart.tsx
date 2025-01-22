import { Box, Button, List } from 'grommet';
import { Add, Checkmark } from 'grommet-icons';
import { ItemCategory } from '../state/Article';
import CartItem from './CartItem';

const shoppingCartData = [
    { code: "123", category: ItemCategory.Beer, description: "Bier, Paul", count: 1, price: 1.10},
    { code: "124", category: ItemCategory.Beer, description: "Bier, Sprint", count: 1, price: 1.20},
    { code: "135", category: ItemCategory.Wine, description: "Prosecco, Volpi", count: 1, price: 12.50 },
    { code: "123", category: ItemCategory.Beer, description: "Bier, Paul", count: 1, price: 1.10},
    { code: "124", category: ItemCategory.Beer, description: "Bier, Sprint", count: 1, price: 1.20},
    { code: "135", category: ItemCategory.Wine, description: "Prosecco, Volpi", count: 1, price: 12.50 },
    { code: "123", category: ItemCategory.Beer, description: "Bier, Paul", count: 1, price: 1.10},
    { code: "124", category: ItemCategory.Beer, description: "Bier, Sprint", count: 1, price: 1.20},
    { code: "135", category: ItemCategory.Wine, description: "Prosecco, Volpi", count: 1, price: 12.50 },
    { code: "123", category: ItemCategory.Beer, description: "Bier, Paul", count: 1, price: 1.10},
    { code: "124", category: ItemCategory.Beer, description: "Bier, Sprint", count: 1, price: 1.20},
    { code: "135", category: ItemCategory.Wine, description: "Prosecco, Volpi", count: 1, price: 12.50 },
    { code: "123", category: ItemCategory.Beer, description: "Bier, Paul", count: 1, price: 1.10},
    { code: "124", category: ItemCategory.Beer, description: "Bier, Sprint", count: 1, price: 1.20},
    { code: "135", category: ItemCategory.Wine, description: "Prosecco, Volpi", count: 1, price: 12.50 },
    { code: "123", category: ItemCategory.Beer, description: "Bier, Paul", count: 1, price: 1.10},
    { code: "124", category: ItemCategory.Beer, description: "Bier, Sprint", count: 1, price: 1.20},
    { code: "135", category: ItemCategory.Wine, description: "Prosecco, Volpi", count: 1, price: 12.50 },
]

const floatingActionBarStyle: React.CSSProperties = {
  position: 'fixed',
  bottom: '20px',
  left:'0', 
  right:'0', 
  margin: 'auto', 
  width: 'fit-content'
};

export const ShoppingCart = () => {
  return (
    <div >
      <List data={shoppingCartData} margin="medium">
          {(item) => (
              <CartItem {...item} />
          )}
      </List>
      <Box direction="row" style={floatingActionBarStyle} >
        <Button icon={<Add/>} primary />
        <Button icon={<Checkmark/>} secondary />
      </Box>
    </div>
    );
};