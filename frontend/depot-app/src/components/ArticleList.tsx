import { List } from 'grommet';
import { Article } from '../state/Article';
import { ArticleItem } from './ArticleItem';

export interface ArticleListProps {
    articles: Article[];
    articleSelected: (article: Article) => void;
};


export const ArticleList = (props: ArticleListProps) => {

    const articleClicked = ({ item, index }: { item: Article; index: number }) => {
        props.articleSelected(item);
    };

    return (

        <List data={props.articles} onClickItem={articleClicked} defaultItemProps={{ pad: 'none'}}>
        {(item) => (
            <ArticleItem {...item} />
        )}
        </List>
    );
};
