import {Box, Button, Paragraph} from 'grommet';
import { headerTitleState } from '../state/NavState';
import { useRecoilState } from 'recoil';
import { useEffect } from 'react';
import { useNavigate } from 'react-router';

export const Home = () => {
    const userName = "Samuel Iseli";  
    const [headerTitle, setHeaderTitle] = useRecoilState<string>(headerTitleState);
    const navigate = useNavigate();

    useEffect(() => {
        setHeaderTitle('Depot Commün');
    }, []);

    return (
        <Box>
            <Paragraph>
                Herzlich willkommen in der Depot-Commün App!
            </Paragraph>
            <Paragraph>
                Du bist angemeldet als {userName}.
            </Paragraph>
            <Paragraph>
                Möchtest Du einen neuen Einkauf erfassen?
            </Paragraph>
            <Button primary label="Einkauf starten" onClick={()=> navigate('/shopping-cart')} />
        </Box>
    );
};

