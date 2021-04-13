import './App.css';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect
} from "react-router-dom";
import Lobby from './Components/Lobby/Lobby';
import LandingPage from './Components/LandingPage/LandingPage';
import Game from './Components/Game/Game'
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  return (
    <Router>
      <Redirect to="/start" />
      <Switch>
        <Route path="/start">
          <LandingPage />
        </Route>
        <Route path="/lobby" component={Lobby}>
        </Route>
        <Route path="/game">
          <Game />
        </Route>
      </Switch>
    </Router >
  );
}

export default App;
