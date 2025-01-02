import { Route, Switch, Router } from 'wouter';
import { Container } from '@mantine/core';
import { Editor } from './pages/editor';
import { Header } from "./components/header";
import { Help } from "./pages/help";
import { Examples } from "./pages/examples";

const links = [
  { link: '/', label: 'Editor' },
  { link: '/examples', label: 'Ejemplos' },
  { link: '/help', label: 'Ayuda' },
];


export const App: React.FC = () => {

  return (
    <Router>
    <Container  size='xl' fluid>
      <Header links={links} />
        <Switch>
          <Route path="/" component={Editor}/>
          <Route path="/examples" component={Examples}/>
          <Route path="/help" component={Help}/>
        </Switch>
    </Container>
    </Router>
  );
};
