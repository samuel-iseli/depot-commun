import React, { createContext, useContext, useState } from 'react';

type BackButtonContextType = {
    setBackButtonCallback: (callback?: () => void) => void;
    backButtonCallback?: () => void;
};

const BackButtonContext = createContext<BackButtonContextType | undefined>(undefined);

export const BackButtonProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [backButtonCallback, setBackButtonCallback] = useState<(() => void) | undefined>(() => () => {});

    return (
        <BackButtonContext.Provider value={{ backButtonCallback, setBackButtonCallback }}>
            {children}
        </BackButtonContext.Provider>
    );
};

export const useBackButton = (): BackButtonContextType => {
    const context = useContext(BackButtonContext);
    if (!context) {
        throw new Error('useBackButton must be used within a BackButtonProvider');
    }
    return context;
};