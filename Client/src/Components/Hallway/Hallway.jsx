import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./Hallway.css";

export class Hallway extends React.Component {

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
            <div className={this.props.orientation === "vertical" ? "hallway-vertical" : "hallway-horizontal"}
                onClick={this.handleClick}>
            </div >
        );
    }
}
export default Hallway;