import { Box, Button, Grid, Text } from 'grommet';
import { Bar, Basket, Cafeteria, Coffee, IceCream, Trash } from 'grommet-icons';
import React from 'react';

export interface ArticleItemProps {
    code: string;
    group: string;
    name: string;
    price: number;
    count: number;
    onRemove?: () => void | undefined;
    onClick?: (e: React.MouseEvent<HTMLElement>) => void | undefined;
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

    // prepare description and amount
    const description = props.count > 1 ? `${props.count} ${props.name}` : props.name
    const amount = props.count > 1 ? (props.price * props.count).toFixed(2) : props.price;

    return (
    <Grid
        align="center"
        rows={['xxsmall']}
        columns={columns}
        gap="none"
        margin="none"
        areas={areas}
        onClick={props.onClick}
        style={{ cursor: props.onClick ? 'pointer' : undefined }}
    >
        <Box gridArea="icon">
            {React.createElement(iconFromGroup(props.group))}
        </Box>
        <Text gridArea="description">{description}</Text>
        <Text gridArea="price" textAlign="end">{amount}</Text>
        {props.onRemove && (
        <Box gridArea="remove" align="end">
            <Button icon={<Trash/>} onClick={e => { e.stopPropagation(); props.onRemove && props.onRemove(); }} />
        </Box>
        )}
    </Grid>
)};

export default ArticleItem;
