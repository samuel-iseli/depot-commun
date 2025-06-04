import { Box, Grid, Text } from 'grommet';
import { Bar, Basket, Cafeteria, Coffee, IceCream, Trash } from 'grommet-icons';
import React from 'react';


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

export interface GroupItemProps {
    name: string;
};

export const GroupItem = (props: GroupItemProps) => {
    const areas = [
        { name: 'icon', start: [0, 0], end: [0, 0] },
        { name: 'description', start: [1, 0], end: [1, 0] },
    ];
    const columns = ['xxsmall', 'auto'];

    return (
    <Grid
        align="center"
        rows={['xxsmall']}
        columns={columns}
        gap="none"
        margin="none"
        areas={areas}>
        <Box gridArea="icon">
            {React.createElement(iconFromGroup(props.name))}
        </Box>
        <Text gridArea="description">{props.name}</Text>        
    </Grid>
)};

export default GroupItem