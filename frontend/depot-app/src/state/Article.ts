import { atom } from 'recoil';

export enum ArticleCategory {
    Beer,
    Wine,
    Beverage,
    Packaged,
    Open,
    Household
}

export type Article =  {
    code: string
    category: ArticleCategory
    description: string
    price: number
}

export const articlesState = atom({
    key: 'articlesState',
    default: [
        <Article>({
            code : "123",
            category: ArticleCategory.Beer,
            description: "Bier, Paul",
            price: 1.10
        }),
        <Article>({
            code : "124",
            category: ArticleCategory.Beer,
            description: "Bier, Sprint",
            price: 1.10
        }),
        <Article>({
            code : "135",
            category: ArticleCategory.Wine,
            description: "Prosecco, Volpi",
            price: 8.50
        }),
    ],
});

export function findArticle(code: string, articles: Article[]): Article | undefined {
    return articles.find(a => a.code == code);
} 
