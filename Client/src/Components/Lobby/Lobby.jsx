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
            playerNames: [
                "player1",
                "player2",
                "player3",
                "player4",
                "player5",
                "player6",
            ]
        }
    }

    render() {
        return (
            <React.Fragment>
                <Card className="playerNamesList" text="white">
                    <ListGroup variant="flush">
                        {this.state.playerNames.map(playerName => (
                            <ListGroup.Item variant="dark">{playerName}</ListGroup.Item>))}
                    </ListGroup>
                </Card >
                <Link to="/game" style={{ textDecoration: 'none' }} >
                    <Button variant="success" className="startButtonSmall lobbyStartButton">
                        <p className="lobbyStartText">
                            Start Game
                        </p>
                    </Button>
                </Link>
                <h2 id="playersReadyText">
                    {this.state.playerNames.length}/{MAX_PLAYERS} Players Present
                </h2>
            </React.Fragment >
        )
    }
}
export default Lobby;