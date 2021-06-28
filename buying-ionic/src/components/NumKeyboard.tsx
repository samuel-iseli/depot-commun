import { IonButton, IonCol, IonGrid, IonRow } from '@ionic/react';

interface KeyProps {
    callback: (value:string) => void,
    children: string
}

interface OkKeyProps {
    callback: (value:string) => void,
    children: string,
    disabled: boolean,
}

const Key: React.FC<KeyProps> = (props) => {
    return (
        <IonButton
            expand="block" color="light" 
            onClick={() => { props.callback(props.children); }}>{props.children}</IonButton>
    );
};

const OkKey: React.FC<OkKeyProps> = (props) => {
    return (
        <IonButton
            expand="block" color="success" disabled={props.disabled}
            onClick={() => { props.callback(props.children); }}>{props.children}</IonButton>
    );
};

interface KeyboardProps {
    okEnabled: boolean,
    callback: (value: string) => void
}

const NumKeyboard: React.FC<KeyboardProps> = (props) => {
  
    return (
        <IonGrid color="grey">
        <IonRow>
          <IonCol><Key callback={props.callback}>7</Key></IonCol>
          <IonCol><Key callback={props.callback}>8</Key></IonCol>
          <IonCol><Key callback={props.callback}>9</Key></IonCol>
        </IonRow>  
        <IonRow>
          <IonCol><Key callback={props.callback}>4</Key></IonCol>
          <IonCol><Key callback={props.callback}>5</Key></IonCol>
          <IonCol><Key callback={props.callback}>6</Key></IonCol>
        </IonRow>  
        <IonRow>
          <IonCol><Key callback={props.callback}>1</Key></IonCol>
          <IonCol><Key callback={props.callback}>2</Key></IonCol>
          <IonCol><Key callback={props.callback}>3</Key></IonCol>
        </IonRow> 
        <IonRow>
          <IonCol><Key callback={props.callback}>Back</Key></IonCol>
          <IonCol><Key callback={props.callback}>0</Key></IonCol>
          <IonCol><OkKey callback={props.callback} disabled={!props.okEnabled}>OK</OkKey></IonCol>
        </IonRow> 
        </IonGrid> 
    );
};

export default NumKeyboard;
