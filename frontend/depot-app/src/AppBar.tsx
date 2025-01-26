import { Header, Menu, Text } from 'grommet';
import { Menu as MenuIcon, Previous } from 'grommet-icons';
import { useNavigate } from 'react-router';
import { useRecoilState } from 'recoil';
import { NavState, navStateAtom } from './state/NavState.ts';

export const AppBar = () => {
    const navigate = useNavigate();
    const [navState, setNavState] = useRecoilState<NavState>(navStateAtom);

    return (
    <Header
        background="brand"
        pad={{ left: "medium", right: "small", vertical: "small" }}
        elevation="medium"
        height="xxsmall"
    >
    { navState.showBackButton ? (
        <Previous onClick={() => navigate(-1)} />
    ) : (
        <Menu icon={<MenuIcon/>}
        items={[
            {label: "Home", onClick: () => { navigate("/"); }},
            {label: "Shopping", onClick: ()=> { navigate("/shopping-cart"); }}
        ]}/>
    ) }
        <Text size="large">Depot App</Text>
    </Header>
    );
};

  