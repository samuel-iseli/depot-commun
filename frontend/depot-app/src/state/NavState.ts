import { atom } from 'recoil';

export const showBackButtonState = atom<boolean>({
    key: 'showBackButton',
    default: false 
});

export const backButtonCallbackState = atom<(() => void) | null>({
    key: 'backButtonCallback',
    default: null
});

export const headerTitleState = atom<string>({
    key: 'headerTitle',
    default: 'Depot Commün'
});
