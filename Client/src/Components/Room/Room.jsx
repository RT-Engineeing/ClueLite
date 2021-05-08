import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./Room.css";
import getUserUUID from '../../UUID/UUID'

import axios from 'axios';
import { Redirect } from 'react-router';

export class Room extends React.Component {

    constructor(props) {
        super(props);
        const pieces = this.props.gameState ?
            this.props.gameState.gameBoard[this.props.y][this.props.x] : [];
        this.state = {
            pieces: pieces,
            charactername: this.props.charactername,
            playerName: this.props.playerName
        }
    }

    handleClick = (event) => {
        event.preventDefault(); // Prevents display of context menu
        if (event.button === 2) {
            if (this.state.pieces.length > 0) {
                let pieces = this.state.pieces;
                pieces.pop();
                this.setState({ pieces })
            }
        } else if (event.button === 0) {
            this.sendMoveRequest();
            // let pieces = this.state.pieces;
            // if (pieces.length === 0) {
            //     pieces.push(1);
            // } else {
            //     pieces.push(this.state.pieces[this.state.pieces.length - 1] + 1);
            // }
            //       this.setState({ pieces });
        }
    }

    async sendMoveRequest() {
        let newX = this.props.x;
        let newY = this.props.y;
        let movingPlayer = this.state.playerName;
        const uuid = getUserUUID();
        const response = await axios.post("http://localhost:5000/movement", {
            x: newY,
            y: newX,
            character: movingPlayer,
            uid: uuid
        });

    }

    render() {

        let pieces = this.props.gameState ?
            this.props.gameState.gameBoard[this.props.y][this.props.x] : [];
        return (
            <div className="room" onClick={this.handleClick} onContextMenu={this.handleClick}>
                <div className="roomName">
                    <p id="regularPiece">{this.props.name}</p>
                </div>
                <span className="gamePieceContainer">
                    {
                        pieces.map((piece, idx) => (
                            <span key={idx} >
                                {piece === this.state.charactername ? <p id="playerPiece">[{piece}]</p> : <p id="regularPiece">[{piece}]</p>}
                            </span>
                        ))
                    }
                </span>
            </div>
        );
    }
}
export default Room;