import React from 'react';
import Card from 'react-bootstrap/Card'
import ListGroup from 'react-bootstrap/ListGroup'
import "./Lobby.css";
import {
    Link,
} from "react-router-dom";
import axios from 'axios';
import Button from 'react-bootstrap/Button';

const MAX_PLAYERS = 6;

export class Lobby extends React.Component {

    constructor(props) {
        super();
        this.state = {
            players: [
            ],
            myPlayer: props.location.state.playername,
            myCurrentReadiness: false,
            sessionKey: props.location.state.sessionKey,
            charactername: props.location.state.charactername,
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

        console.log("props: " + JSON.stringify(this.props));
        console.log("state: " + JSON.stringify(this.state));
        await this.pollForReadinessStatuses();
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
            <React.Fragment id="lobbyContainer">
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
            </React.Fragment >
        )
    }
}
export default Lobby;