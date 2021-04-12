import React from 'react';
import Card from 'react-bootstrap/Card'
import ListGroup from 'react-bootstrap/ListGroup'
import "./Lobby.css";
import {
    Link,
} from "react-router-dom";
import axios from 'axios';
import Button from 'react-bootstrap/Button';
import getUserUUID from '../../UUID/UUID';

const MAX_PLAYERS = 6;

export class Lobby extends React.Component {

    constructor(props) {
        super();
        this.state = {
            players: [
                ["Player1", false],
                ["Player2", false],
                ["Player3", false],
                ["Player4", false],
                ["Player5", false],
                ["Player6", false],
            ],
            myPlayer: props.location.state.playername, // These props come from the Router/Switch
            sessionKey: props.location.state.sessionKey,
            myCurrentReadiness: false,
            gameCanStart: false
        }
    }

    toggleReadiness() {
        this.state.ready = !this.state.ready;
    }

    async pollForReadinessStatuses() {
        const response = await axios.get("http://localhost:5000/ready");

        const responseData = response.data;

        const readyPlayers = responseData["playersready"];
        let playersCopy = [...this.state.players];

        playersCopy.forEach(player => {
            player[1] = readyPlayers.includes(player[0]) ? true : false;
        });

        this.setState({
            gameCanStart: responseData["status"] !== "false",
            players: playersCopy
        });
    }


    async changeReadiness() {
        let newReadiness = !this.state.myCurrentReadiness;
        let readinessTransmit = newReadiness ? "True" : "False";
        const response = await axios.post("http://localhost:5000/ready", {
            playername: this.state.myPlayer,
            sessionId: this.state.sessionKey,
            playerready: readinessTransmit
        });
    }

    async componentDidMount() {
        this.interval = setInterval(() => this.pollForReadinessStatuses(), 1000);
    }

    componentWillUnmount() {
        clearInterval(this.interval);
    }


    handleClick = (event) => {
        this.changeReadiness();
    }

    render() {
        const startButton = (
            <Button variant="success" disabled={!this.state.gameCanStart} className="lobbyStartButton">
                <p className="lobbyStartText">
                    Start Game
            </p>
            </Button>
        );

        const waitingButton = (
            <Button variant="success" disabled={!this.state.gameCanStart} className="lobbyWaitingButton">
                <p className="lobbyWaitingText">
                    Waiting for more players..
                </p>
            </Button>
        )
        return (
            <div id="lobbyContainer">
                <Card className="playerNamesList" text="white">
                    <ListGroup variant="flush">
                        {this.state.players.map(player => (
                            <ListGroup.Item key={player[0]} variant="dark" >
                                {player[0] === this.state.myPlayer ? <span className="myPlayer">*</span> : ""}
                                {player[0]}
                                <Button onClick={this.handleClick}
                                    className={player[1] ? "readyButton" : "notReadyButton"} >
                                </Button>
                            </ListGroup.Item>))}
                    </ListGroup>
                </Card >
                <Link to="/game" style={{ textDecoration: 'none' }} >
                    {this.state.gameCanStart ? startButton : waitingButton}
                </Link>
                <h2 id="playersReadyText">
                    {this.state.players.length}/{MAX_PLAYERS} Players Present
                </h2>
            </div >
        )
    }
}
export default Lobby;