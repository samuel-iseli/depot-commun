import { Box, Button, Grid } from 'grommet';
import { Basket, Trash } from 'grommet-icons';
import React from 'react';

export interface ArticleItemProps {
    code: string;
    group: string;
    name: string;
    price: number;
    onRemove?: () => void | undefined;
}

const iconFromGroup = (group : string) => {
    if (group == "Beer") {
        return Basket;
    } 
    if (group == "Wine") {
        return Basket;
    }
    else
        return Basket;
};

export const ArticleItem = (props: ArticleItemProps) => {
    const areas = [
        { name: 'icon', start: [0, 0], end: [0, 0] },
        { name: 'description', start: [1, 0], end: [1, 0] },
        { name: 'price', start: [2, 0], end: [2, 0] },
    ];
    const columns = ['xxsmall', 'auto', 'xsmall'];

    if (typeof props.onRemove === 'function') {
        areas.push({ name: 'remove', start: [3, 0], end: [3, 0] });
        columns.push('xxsmall');
    };

    return (
    <Grid
        align="center"
        
        rows={['xxsmall']}
        columns={columns}
        gap="small"
        areas={areas}>
        <Box gridArea="icon">
            {React.createElement(iconFromGroup(props.group))}
        </Box>
        <Box gridArea="description" >
            {props.name}        
        </Box>
        <Box gridArea="price" align="end">
            {props.price}
        </Box>

        {props.onRemove && (
        <Box gridArea="remove" align="end">
            <Button icon={<Trash/>} onClick={() => props.onRemove && props.onRemove()}/>
        </Box>)}
    </Grid>
)};

export default ArticleItem;
