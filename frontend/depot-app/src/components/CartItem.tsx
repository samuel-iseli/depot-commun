import { Box, Grid } from 'grommet';
import { ItemCategory } from '../state/Article';
import { Basket, Trash } from 'grommet-icons';
import React from 'react';

interface CartItemProps {
    code: string;
    category: ItemCategory;
    description: string;
    price: number;
    count: number;
}

const iconFromCategory = (cat : ItemCategory) => {
    if (cat == ItemCategory.Beer) {
        return Basket;
    } 
    if (cat == ItemCategory.Wine) {
        return Basket;
    }
    else
        return Basket;
};

const CartItem = (props: CartItemProps) => (
    <Grid
        align="center"
        
        rows={['xxsmall']}
        columns={['xxsmall', 'auto', 'xsmall', 'xxsmall']}
        gap="small"
        areas={[
        { name: 'icon', start: [0, 0], end: [0, 0] },
        { name: 'description', start: [1, 0], end: [1, 0] },
        { name: 'price', start: [2, 0], end: [2, 0] },
        { name: 'remove', start: [3, 0], end: [3, 0] },
        ]}
    >
        <Box gridArea="icon">
            {React.createElement(iconFromCategory(props.category))}
        </Box>
    
        <Box gridArea="description" >
            {props.description}        
        </Box>
    
        <Box gridArea="price" align="end">
            {props.price}
        </Box>

        <Box gridArea="remove" align="end">
            <Trash/>
        </Box>
    </Grid>
);

export default CartItem;
