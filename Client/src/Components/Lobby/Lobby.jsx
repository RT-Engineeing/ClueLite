import React from 'react';
import Card from 'react-bootstrap/Card'
import ListGroup from 'react-bootstrap/ListGroup'
import "./Lobby.css";
import {
    Link,
} from "react-router-dom";
import Button from 'react-bootstrap/Button';

const MAX_PLAYERS = 6;

export class Lobby extends React.Component {

    constructor(props) {
        super();
        this.state = {
            players: [
                ["Player1", "false"],
                ["Player2", "false"],
                ["Player3", "false"],
                ["Player4", "false"],
                ["Player5", "false"],
                ["Player6", "false"],
            ]
        }
    }

    render() {
        return (
            <React.Fragment>
                <Card className="playerNamesList" text="white">
                    <ListGroup variant="flush">
                        {this.state.players.map(player => (
                            <ListGroup.Item key={player[0]} variant="dark">

                                {player[0]} &#x1F534;

                            </ListGroup.Item>))}
                    </ListGroup>
                </Card >
                <Link to="/game" style={{ textDecoration: 'none' }} >
                    <Button variant="success" className="lobbyStartButton">
                        <p className="lobbyStartText">
                            Start Game
                        </p>
                    </Button>
                </Link>
                <h2 id="playersReadyText">
                    {this.state.players.length}/{MAX_PLAYERS} Players Present
                </h2>
            </React.Fragment >
        )
    }
}
export default Lobby;