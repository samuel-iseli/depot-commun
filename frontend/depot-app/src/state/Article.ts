import {selector } from 'recoil';

export type Article =  {
    code: string
    group: string
    name: string
    price: number
    id: number
}

// export const activeArticles = atom({
//     key: 'articlesState',
//     default: [
//         <Article>({
//             code : "123",
//             group: "Beer",
//             name: "Bier, Paul",
//             price: 1.10
//         }),
//         <Article>({
//             code : "124",
//             group: "Beer",
//             name: "Bier, Sprint",
//             price: 1.10
//         }),
//         <Article>({
//             code : "135",
//             group: "Wine",
//             name: "Prosecco, Volpi",
//             price: 8.50
//         }),
//     ],
// });

export const activeArticles = selector({
    key: 'activeArticles',
    get: async () => {
        const response = await fetch('http://localhost:8000/api/active_articles');
        return response.json();
    }
})

export const activeGroups = selector({
    key: 'activeGroups', 
    get: async () => {
        const response = await fetch('http://localhost:8000/api/active_groups');    
        return response.json();
    }
})

export function findArticle(code: string, articles: Article[]): Article | undefined {
    return articles.find(a => a.code == code);
} 
