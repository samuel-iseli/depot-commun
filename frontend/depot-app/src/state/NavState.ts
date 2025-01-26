import { atom } from 'recoil';

export type NavState = 
    {
        showBackButton: boolean
    }

export const navStateAtom = atom<NavState>({
    key: 'navState',
    default: {
        showBackButton: false
    }   
});
