import { useNavigate } from 'react-router';
import { Box, Button, List, Notification, Text } from 'grommet';
import { Add, Checkmark } from 'grommet-icons';
import { useRecoilState } from 'recoil';
import { cartState } from '../state/Cart';
import ArticleItem from '../components/ArticleItem';
import { headerTitleState } from '../state/NavState';
import { useEffect, useState } from 'react';
import { Drop, Form, FormField } from 'grommet';

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
  const [headerTitle, setHeaderTitle] = useRecoilState<string>(headerTitleState);
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null);
  const [editCount, setEditCount] = useState<string>('');
  const [showDialog, setShowDialog] = useState(false);
  const [dropTarget, setDropTarget] = useState<HTMLElement | null>(null);

  const removeItem = (index: number) => {
    const newCartItems = cartItems.slice();
    newCartItems.splice(index, 1)
    setCartItems(newCartItems);
  }

  const handleItemClick = (index: number, event: React.MouseEvent<HTMLElement>) => {
    setSelectedIndex(index);
    setEditCount(cartItems[index]?.count?.toString() || '1');
    setShowDialog(true);
    setDropTarget(event.currentTarget as HTMLElement);
  };

  const handleDialogSave = () => {
    if (selectedIndex !== null) {
      const newCartItems = cartItems.slice();
      const count = parseInt(editCount, 10);
      if (!isNaN(count) && count > 0) {
        newCartItems[selectedIndex] = { ...newCartItems[selectedIndex], count };
        setCartItems(newCartItems);
      }
    }
    setShowDialog(false);
    setSelectedIndex(null);
  };

  const handleDialogCancel = () => {
    setShowDialog(false);
    setSelectedIndex(null);
  };

  useEffect(() => {
    setHeaderTitle('Warenkorb');
  }, []);

  return (
    <>
      <List data={cartItems} defaultItemProps={{ pad: 'none'}} >
          {(item, index) => (
              <ArticleItem {...item} onRemove={() => removeItem(index)} onClick={(e: React.MouseEvent<HTMLElement>) => handleItemClick(index, e)} />
          )}
      </List>
      {cartItems.length === 0 &&
      <Notification status="info" title="Artikel hinzufügen" message="Clicke auf den + Button unten, um einen Artikel zu erfassen"/>}
      <Box direction="row" style={floatingActionBarStyle} >
        <Button icon={<Add/>} primary onClick={() => navigate('/add-cart-item')} />
        <Button icon={<Checkmark/>} secondary onClick={() => navigate('/finish-purchase')} />
      </Box>
      {showDialog && dropTarget && (
        <Drop target={dropTarget} align={{ top: 'bottom' }} margin="small" 
          stretch={false}
          elevation="small" background="" onClickOutside={handleDialogCancel} onEsc={handleDialogCancel}>
          <Box pad="medium" gap="small" width="medium">
            <Form
              onSubmit={e => {
                e.preventDefault();
                handleDialogSave();
              }}
            >
              <FormField label="Anzahl">
                <Box direction="row" align="center" gap="small">
                  <Button label="-" onClick={() => setEditCount(prev => Math.max(1, parseInt(prev || '1', 10) - 1).toString())} />
                  <Text>{editCount}</Text>
                  <Button label="+" onClick={() => setEditCount(prev => (parseInt(prev || '1', 10) + 1).toString())} />
                </Box>
              </FormField>
              <Box direction="row" gap="small" justify="end" margin={{ top: 'medium' }}>
                <Button label="Abbrechen" onClick={handleDialogCancel} />
                <Button type="submit" label="Speichern" primary />
              </Box>
            </Form>
          </Box>
        </Drop>
      )}
    </>
    );
};