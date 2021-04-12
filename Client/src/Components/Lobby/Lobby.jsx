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
                ["Player1", "false"],
                ["Player2", "false"],
                ["Player3", "false"],
                ["Player4", "false"],
                ["Player5", "false"],
                ["Player6", "false"],
            ],
            myPlayer: "Player1",
            myCurrentReadiness: false;
            sessionKey: "session"
        }
    }

    toggleReadiness() {
        this.state.ready = !this.state.ready;
    }

    async pollForReadinessStatuses() {
        const response = await axios.get("http://localhost:5000/ready");

        const playerArray = response.data;

        this.setState({
            players: playerArray
        })

        console.log("player array: " + playerArray);


        setTimeout(async () => {
            await this.pollForReadinessStatuses();
        }, 5000);
    }

    async changeReadiness() {

        let newReadiness = !this.state.myCurrentReadiness;

        const response = await axios.post("http://localhost:5000/ready", {
            playername: this.state.myPlayer,
            sessionKey: this.state.sessionKey,
            playerready: newReadiness
        });

        console.log("readiness change response: " + response);


    }

    changeReadiness = () => {

    }

    render() {

        return (
            <React.Fragment>
                <Card className="playerNamesList" text="white">
                    <ListGroup variant="flush">
                        {this.state.players.map(player => (
                            <ListGroup.Item key={player[0]} variant="dark">


                                {player[0]}


                                {player[1] === "false" ? "&#x1F534;" : "&#x1F7E2;"}

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