import { List } from 'grommet';
import { GroupItem } from './GroupItem';    

export interface ArticleGroupListProps {
    groups: string[]; 
    groupSelected: (group: string) => void;
};

export const ArticleGroupList = (props: ArticleGroupListProps) => {

    const groupClicked = ({ item, index }: { item: string; index: number }) => {
        props.groupSelected(item);
    };

    return (

        <List data={props.groups} onClickItem={groupClicked} defaultItemProps={{ pad: 'none'}}>
        {(item) => (
            <GroupItem name={item} />
        )}
        </List>
    );
};
