import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./Room.css";

export class Room extends React.Component {

    constructor(props) {
        super(props);
        console.log(`x =${props.x}`)
        console.log(`y =${props.y}`)
        console.log(`roomName =${props.name}`)
    }

    handleClick = (button) => {
        let name = this.props.name;
        console.log(`clicked on room ${name}`);
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