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
                ["Player1", "False"],
                ["Player2", "False"],
                ["Player3", "False"],
                ["Player4", "False"],
                ["Player5", "False"],
                ["Player6", "False"],
            ],
            myPlayer: props.location.state.playerName,
            myCurrentReadiness: false,
            sessionKey: props.location.state.sessionKey,
            gameCanStart: false
        }
    }



    // static getDerivedStateFromProps(props, state){
    //     if(props.players !== state.propsPlayers) {
    //         return {
    //             players: props.players,
    //             propsPlayers: props.players
    //         }
    //     }
    // }

    toggleReadiness() {
        this.state.ready = !this.state.ready;
    }

    async pollForReadinessStatuses() {
        const response = await axios.get("http://localhost:5000/ready");

        const responseData = response.data;

        const readyPlayers = responseData["playersready"];
        let playersCopy = [...this.state.players];


        var i;
        for(i = 0; i < 6; i++){
            var j;
            let player = playersCopy[i];
            for(j = 0; j < readyPlayers.length; j++){
                if(player[0] === readyPlayers[j]){
                    player[1] = "True"; 
                    playersCopy[i] = player;
                }
            }
        }

        console.log("state: " + JSON.stringify(this.state));
        
        this.setState({
            gameCanStart: responseData["status"],
            players: playersCopy
        });

        setTimeout(async () => {
            await this.pollForReadinessStatuses();
        }, 5000);
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

    async componentDidMount(){

        console.log("props: " + JSON.stringify(this.props));
        console.log("state: " + JSON.stringify(this.state));
        await this.pollForReadinessStatuses();

    }


    handleClick = (event) => {
        event.preventDefault(); // Prevents display of context menu
        if (event.button === 2) {
          
        } else if (event.button === 0) {
            this.changeReadiness();
        }
    }

    render() {
        console.log("rendering with player " + this.state.myPlayer + " and session " + this.state.sessionKey);
        return (
            <div>
                <Card className="playerNamesList" text="white">
                    <ListGroup variant="flush">
                        {this.state.players.map(player => (
                            <ListGroup.Item key={player[0]} variant="dark">


                                {player[0]} {player[1]}

                                <Button onClick={this.handleClick}> 

                                    {player[1] === "False" ? "\uD83D\uDD34" : "\uD83D\uDFE2"}
                                </Button>
                            </ListGroup.Item>))}
                    </ListGroup>
                </Card >
                <Link to="/game" style={{ textDecoration: 'none' }} >
                    <Button variant="success" disabled={!this.state.gameCanStart} className="lobbyStartButton">
                        <p className="lobbyStartText">
                            Start Game
                        </p>
                    </Button>
                </Link>
                <h2 id="playersReadyText">
                    {this.state.players.length}/{MAX_PLAYERS} Players Present
                </h2>
            </div >
        )
    }
}
export default Lobby;