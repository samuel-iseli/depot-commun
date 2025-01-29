import { Box, Button, Grid, Text } from 'grommet';
import { Bar, Basket, Cafeteria, Coffee, IceCream, Trash } from 'grommet-icons';
import React from 'react';

export interface ArticleItemProps {
    code: string;
    group: string;
    name: string;
    price: number;
    onRemove?: () => void | undefined;
}

const iconFromGroup = (group : string) => {
    switch (group) { 
    case "Food":
        return Cafeteria;   
    case "Getränke":
        return Bar;
    case "Süsses & Snacks":
        return IceCream; 
    default:
        return Basket;   
    };
}

export const ArticleItem = (props: ArticleItemProps) => {
    const areas = [
        { name: 'icon', start: [0, 0], end: [0, 0] },
        { name: 'description', start: [1, 0], end: [1, 0] },
        { name: 'price', start: [2, 0], end: [2, 0] },
    ];
    const columns = ['xxsmall', 'auto', 'xxsmall'];

    if (typeof props.onRemove === 'function') {
        areas.push({ name: 'remove', start: [3, 0], end: [3, 0] });
        columns.push('xxsmall');
    };

    return (
    <Grid
        align="center"
        rows={['xxsmall']}
        columns={columns}
        gap="none"
        margin="none"
        areas={areas}>
        <Box gridArea="icon">
            {React.createElement(iconFromGroup(props.group))}
        </Box>
        <Text gridArea="description">{props.name}</Text>        
        <Text gridArea="price" textAlign="end">{props.price}</Text>

        {props.onRemove && (
        <Box gridArea="remove" align="end">
            <Button icon={<Trash/>} onClick={() => props.onRemove && props.onRemove()}/>
        </Box>)}
    </Grid>
)};

export default ArticleItem;
