import { Article } from "../state/Article";
import { ArticleList } from "./ArticleList";
import { ArticleGroupList } from "./ArticleGroupList";
import { useEffect, useState } from "react";
import { useBackButton } from '../context/BackButtonContext';

export interface ArticleSelectorProps {
    groups: string[];
    articles: Article[];
    articleSelected: (article: Article) => void;
};

export const ArticleSelector = (props: ArticleSelectorProps) => {
    const [articleSelection, setArticleSelection] = useState<boolean>(false);
    const [articles, setArticles] = useState<Article[]>([]);
    const { setBackButtonCallback } = useBackButton();


    const groupSelected = (group: string) => {
        setArticleSelection(true);
        setArticles(props.articles.filter(a => a.group == group));
    };

    useEffect(() => {
        if ( articleSelection) {
            setBackButtonCallback(() => () => {
                setArticleSelection(false);
                setArticles([]);
            })
        }

        // Cleanup: Reset to default back button action
        return () => setBackButtonCallback(undefined);
    }, [articleSelection, setBackButtonCallback]);

    return (
        articleSelection ? (
            <ArticleList articles={articles} articleSelected={props.articleSelected} />
            ) : (
            <ArticleGroupList groups={props.groups} groupSelected={groupSelected} />
        )
    );  
};
