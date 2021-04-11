import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./Hallway.css";
import GamePieceContainer from '../GamePieceContainer/GamePieceContainer';

export class Hallway extends React.Component {

    constructor(props) {
        super(props);
    }

    handleClick = (button) => {
        // console.log(this.props.x);
        // console.log(this.props.y);
    }

    render() {
        const classNames = `gamePieceContainer ${this.props.orientation === "vertical" ? "hallwayPieceVertical" : "hallwayPieceHorizontal"}`;
        return (
            <div className={this.props.orientation === "vertical" ? "hallway-vertical" : "hallway-horizontal"}
                onClick={this.handleClick}>
                <span className={classNames}>
                    <GamePieceContainer />
                </span>
            </div >
        );
    }
}
export default Hallway;