import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./Room.css";
import RoomImage from '../../Images/room.png'

export class Room extends React.Component {

    constructor(props) {
        super(props);
        console.log(`x =${props.x}`)
        console.log(`y =${props.y}`)
        console.log(`roomName =${props.name}`)
    }

    handleClick = (button) => {
        console.log("Clicked button");
    }

    render() {
        return (
            <div>
                <div className="room" onClick={this.handleClick} >
                    {this.props.name}
                </div>
            </div>
        );
    }
}
export default Room;