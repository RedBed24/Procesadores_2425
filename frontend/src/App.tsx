import { Route, Switch, Router } from 'wouter';
import { Container } from '@mantine/core';
import { EditorPartitune } from './pages/editor';
import { Header } from "./components/header";
import { Help } from "./pages/help";
import { Examples } from "./pages/examples";

const links = [
  { link: '/', label: 'Editor' },
  // { link: '/examples', label: 'Ejemplos' },
  { link: '/help', label: 'Autores' },
];


export const App: React.FC = () => {

  return (
    <Router>
    <Container size='xl' fluid p={0}>
      <Header links={links} />
        <Switch>
          <Route path="/" component={EditorPartitune}/>
          <Route path="/examples" component={Examples}/>
          <Route path="/help" component={Help}/>
        </Switch>
    </Container>
    </Router>
  );
};
