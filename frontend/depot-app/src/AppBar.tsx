import { Header, Menu, Text } from 'grommet';
import { Menu as MenuIcon, Previous } from 'grommet-icons';
import { useNavigate } from 'react-router';
import { useRecoilValue } from 'recoil';
import { headerTitleState, showBackButtonState } from './state/NavState.ts';

export const AppBar = () => {
    const navigate = useNavigate();
    const showBackButton = useRecoilValue<boolean>(showBackButtonState);
    const title = useRecoilValue<string>(headerTitleState);

    return (
    <Header
        background="brand"
        pad={{ left: "medium", right: "medium", vertical: "small" }}
        elevation="medium"
        height="xxsmall"
    >
    { showBackButton ? (
        <Previous onClick={() => navigate(-1)} />
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

  