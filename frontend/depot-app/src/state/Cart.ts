import { atom, useRecoilState } from 'recoil';
import { Article } from './Article';


export const cartState = atom({
    key: 'cartState',
    default: new Array<Article>(),
})

export const addArticleToCart = (article: Article) => {
    const [cart, setCart] = useRecoilState(cartState);

    setCart([...cart, article]);
}   

