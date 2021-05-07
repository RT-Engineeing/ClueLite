import React from 'react';
import Card from 'react-bootstrap/Card'
import ListGroup from 'react-bootstrap/ListGroup'
import InputGroup from 'react-bootstrap/InputGroup'
import FormControl from 'react-bootstrap/FormControl'
import "./Lobby.css";
import {
    Link, Redirect
} from "react-router-dom";
import axios from 'axios';
import Button from 'react-bootstrap/Button';

const MAX_PLAYERS = 6;

export class Lobby extends React.Component {

    componentWillReceiveProps(nextProps) {
        this.setState({
            myPlayer: nextProps.location.state.playername,
            sessionKey: nextProps.location.state.sessionKey,
            uuid: nextProps.location.state.uuid,
            charactername: nextProps.location.state.charactername,
            cards: undefined
        });
    }

    constructor(props) {
        super();
        this.state = {
            players: [
            ],
            myCurrentReadiness: false,
            gameCanStart: false,
            pollingForGameState: false,
            myPlayer: props.location.state.playername,
            sessionKey: props.location.state.sessionKey,
            uuid: props.location.state.uuid,
            charactername: props.location.state.charactername,
            playerAlias: props.location.state.playername,
            isEditingName: false
        }
        // Gets card info
        this.getCards();
    }


    async pollForGameState() {

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

        const readyPlayers = responseData["playersready"];
        const playersList = responseData["lobbyPlayers"];



        let lobbyData = [];

        playersList.forEach(player => {
            let readyStatus = readyPlayers.includes(player) ? true : false;
            lobbyData.push([player, readyStatus]);
        });

        this.setState({
            gameCanStart: responseData["status"] !== "false",
            players: lobbyData
        });

        if (this.state.gameCanStart && !this.state.pollingForGameState) {
            this.gameStateInterval = setInterval(() => this.pollForGameState(), 1000);
            this.setState({
                pollingForGameState: true
            })
        }
    }

    getCards = async () => {
        const response = await axios.get("http://localhost:5000/cards",
            {
                params: {
                    uid: this.state.uuid
                }
            });
        this.state.cards = JSON.parse(response.data);
    }



    async changeReadiness() {
        let newReadiness = !this.state.myCurrentReadiness;
        let readinessTransmit = newReadiness ? "True" : "False";
        const response = await axios.post("http://localhost:5000/ready", {
            playername: this.state.myPlayer,
            sessionId: this.state.sessionKey,
            playerready: readinessTransmit,
            playerAlias: this.state.playerAlias,
            uid: this.state.uuid
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

    toggleEditing = (event) => {
        this.setState({ isEditingName: !this.state.isEditingName })
    }

    handleClick = (event) => {
        this.changeReadiness();
    }

    onUpdateAlias = (event) => {
        event.preventDefault();
        this.setState({
            playerAlias: document.getElementById('playerAliasInput').value,
            isEditingName: false
        }, () => { this.changeReadiness() });
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
        if (this.state.pollingForGameState) {
            return (
                <Redirect to={{
                    pathname: "/game",
                    state: {
                        playerName: this.state.myPlayer,
                        charactername: this.state.charactername,
                        uuid: this.state.uuid,
                        sessionkey: this.state.sessionKey,
                        characters: this.state.cards.characters,
                        weapons: this.state.cards.weapons,
                        rooms: this.state.cards.rooms,
                        imageURLs: this.state.cards.imageURLs,
                    }
                }}></Redirect>
            )
        } else {

            const myPlayer =
                (<span className="myPlayer">
                    <button className="editNameButton" onClick={this.toggleEditing}>
                        <i class="fa fa-lg fa-edit editNameIcon" ></i >
                    </button >
                </span >);


            return (
                <React.Fragment key="lobbyContainer">
                    <Card className="playerNamesList" text="white">
                        <ListGroup variant="flush">
                            {this.state.players.map(player => (
                                <ListGroup.Item key={player[0]} variant="dark" >
                                    {player[0] === this.state.playerAlias ?
                                        myPlayer
                                        : ""}
                                    {this.state.isEditingName && player[0] === this.state.playerAlias ?
                                        <InputGroup className="mb-3">
                                            <form onSubmit={this.onUpdateAlias}>
                                                <FormControl
                                                    placeholder={player[0]}
                                                    aria-label="Player Alias"
                                                    aria-describedby="basic-addon2"
                                                    id="playerAliasInput"
                                                />
                                            </form>
                                        </InputGroup>
                                        :
                                        player[0]
                                    }
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