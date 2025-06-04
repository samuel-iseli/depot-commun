import { Header, Menu, Text } from 'grommet';
import { Menu as MenuIcon, Previous } from 'grommet-icons';
import { useNavigate } from 'react-router';
import { useRecoilValue } from 'recoil';
import { useBackButton } from './context/BackButtonContext';
import { headerTitleState, showBackButtonState } from './state/NavState';

export const AppBar = () => {
    const navigate = useNavigate();
    const showBackButton = useRecoilValue<boolean>(showBackButtonState);
    const { backButtonCallback } = useBackButton();
    const title = useRecoilValue<string>(headerTitleState);

    return (
    <Header
        background="brand"
        pad={{ left: "medium", right: "medium", vertical: "small" }}
        elevation="medium"
        height="xxsmall"
    >
    { showBackButton ? (
        <Previous onClick={() =>  {
            if (backButtonCallback !== undefined) {
                backButtonCallback();
            } else {
                navigate(-1);   
            }
        }} />
    ) : (
        <Menu icon={<MenuIcon/>}
        items={[
            {label: "Home", onClick: () => { navigate("/"); }},
            {label: "Shopping", onClick: ()=> { navigate("/shopping-cart"); }}
        ]}/>
    ) }
        <Text size="large">{title}</Text>
    </Header>
    );
};

  