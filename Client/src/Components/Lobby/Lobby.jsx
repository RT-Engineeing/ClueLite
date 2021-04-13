import React from 'react';
import Card from 'react-bootstrap/Card'
import ListGroup from 'react-bootstrap/ListGroup'
import "./Lobby.css";
import {
    Link, Redirect
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
            gameCanStart: false,
            pollingForGameState: false,
            uuid: props.location.state.uuid
        }
    }


    async pollForGameState() {

        console.log('in poller');
        const response = await axios.post("http://localhost:5000/getstate", {
            uid: this.state.uuid
        });

        const gamestate = response.data;

        const gamerunning = gamestate["gamerunning"];

        if (gamerunning) {
            /**
             * INSERT LINK TO FORCE ALL PLAYERS INTO GAMEBOARD HERE
             */
        }

    }

    async pollForReadinessStatuses() {
        const response = await axios.get("http://localhost:5000/ready");

        const responseData = response.data;

        console.log("Response data: " + JSON.stringify(responseData));

        const readyPlayers = responseData["playersready"];
        const playersList = responseData["lobbyPlayers"];



        let lobbyData = [];

        playersList.forEach(player => {
            let readyStatus = readyPlayers.includes(player) ? true : false;
            lobbyData.push([player, readyStatus]);
        });

        console.log("ready status: " + JSON.stringify(lobbyData));

        this.setState({
            gameCanStart: responseData["status"] !== "false",
            players: lobbyData
        });

        console.log("gamecanstart: " + this.state.gameCanStart + ", polling? " + this.state.pollingForGameState);
        if (this.state.gameCanStart && !this.state.pollingForGameState) {
            console.log("setting interval for game state polling");
            this.gameStateInterval = setInterval(() => this.pollForGameState(), 1000);
            this.setState({
                pollingForGameState: true
            })
        }
    }


    async changeReadiness() {
        let newReadiness = !this.state.myCurrentReadiness;
        let readinessTransmit = newReadiness ? "True" : "False";
        const response = await axios.post("http://localhost:5000/ready", {
            playername: this.state.myPlayer,
            sessionId: this.state.sessionKey,
            playerready: readinessTransmit
        });

        this.setState({
            myCurrentReadiness: newReadiness
        });
    }

    async componentDidMount() {
        this.interval = setInterval(() => this.pollForReadinessStatuses(), 1000);
    }

    componentWillUnmount() {
        clearInterval(this.interval);
        clearInterval(this.gameStateInterval);
    }



    handleClick = (event) => {
        this.changeReadiness();
    }

    render() {
        console.log(this.state);
        console.log(this.props);
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
        if (this.state.pollingForGameState) {
            return (
                <Redirect to={{pathname: "/game",
                                state: {
                                    playerName: this.state.myPlayer,
                                    charactername: this.state.charactername,
                                    uuid: this.state.uuid,
                                    sessionkey: this.state.sessionKey
                                }}}></Redirect>
            )
        } else {
            return (
                <React.Fragment key="lobbyContainer">
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
}
export default Lobby;