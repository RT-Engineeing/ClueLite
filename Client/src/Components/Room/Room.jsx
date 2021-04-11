import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./Room.css";
import GamePieceContainer from '../GamePieceContainer/GamePieceContainer';

export class Room extends React.Component {

    constructor(props) {
        super(props);
    }

    handleClick = (button) => {
    }

    render() {
        return (
            <div className="room" onClick={this.handleClick} >
                <div className="roomName">
                    {this.props.name}
                </div>
                <span className="gamePieceContainer">
                    <GamePieceContainer />
                </span>
            </div>
        );
    }
}
export default Room;