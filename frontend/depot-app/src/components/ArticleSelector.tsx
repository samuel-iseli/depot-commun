import { Article } from "../state/Article";
import { ArticleList } from "./ArticleList";
import { ArticleGroupList } from "./ArticleGroupList";
import { useState } from "react";

export interface ArticleSelectorProps {
    groups: string[];
    articles: Article[];
    articleSelected: (article: Article) => void;
};


export const ArticleSelector = (props: ArticleSelectorProps) => {
    const [articleSelection, setArticleSelection] = useState<boolean>(false);
    const [articles, setArticles] = useState<Article[]>([]);

    const groupSelected = (group: string) => {
        setArticleSelection(true);
        setArticles(props.articles.filter(a => a.group == group));
    };

    return (
        articleSelection ? (
            <ArticleList articles={articles} articleSelected={props.articleSelected} />
            ) : (
            <ArticleGroupList groups={props.groups} groupSelected={groupSelected} />
        )
    );  
};
