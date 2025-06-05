import { atom, useRecoilState } from 'recoil';
import { Article } from './Article';


export const cartState = atom({
    key: 'cartState',
    default: new Array<Article>(),
})

// Utility to add an article to the cart with count defaulting to 1 if not set
export const addArticleToCart = (article: Article) => {
    const [cart, setCart] = useRecoilState(cartState);
    setCart([...cart, { ...article, count: article.count ?? 1 }]);
}

