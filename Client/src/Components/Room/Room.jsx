import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./Room.css";
import RoomImage from '../../Images/room.png'

export class Room extends React.Component {
    render() {
        return (
            <div>
                <img src={RoomImage} alt='Room' className="room" />
            </div>
        );
    }
}
export default Room;