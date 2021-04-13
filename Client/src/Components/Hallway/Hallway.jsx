import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./Hallway.css";

export class Hallway extends React.Component {

    constructor(props) {
        super(props);
        const pieces = this.props.gameState ?
            this.props.gameState.gameBoard[this.props.y][this.props.x] : [];
        this.state = {
            pieces
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
            let pieces = this.state.pieces;
            if (pieces.length === 0) {
                pieces.push(1);
            } else {
                pieces.push(this.state.pieces[this.state.pieces.length - 1] + 1);
            }
            this.setState({ pieces });
        }
    }

    render() {
        const classNames = `gamePieceContainer ${this.props.orientation === "vertical" ? "hallwayPieceVertical" : "hallwayPieceHorizontal"}`;
        return (
            <div className={this.props.orientation === "vertical" ? "hallway-vertical" : "hallway-horizontal"}
                onClick={this.handleClick} onContextMenu={this.handleClick} >
                <span className={classNames}>
                    {
                        this.state.pieces.map((piece, idx) => (
                            <div key={idx}>
                                [{piece}]
                            </div>
                        ))
                    }
                </span>
            </div >
        );
    }
}
export default Hallway;