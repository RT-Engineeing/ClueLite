import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./Hallway.css";

export class Hallway extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            pieces: [1]
        }
    }

    handleEvent = (event) => {
        if (event.type === "mousedown") {
            this.mouseDown = true;
            this.mouseDownTime = performance.now();
        } else {
            this.mouseDown = false;
            const clickDuration = performance.now() - this.mouseDownTime;
            if (clickDuration > 250.0) {
                if (this.state.pieces.length > 0) {
                    let pieces = this.state.pieces;
                    pieces.pop();
                    this.setState({ pieces })
                }
            } else {
                let pieces = this.state.pieces;
                pieces.push(this.state.pieces[this.state.pieces.length - 1] + 1)
                this.setState({ pieces })
            }
        }
    }

    render() {
        const classNames = `gamePieceContainer ${this.props.orientation === "vertical" ? "hallwayPieceVertical" : "hallwayPieceHorizontal"}`;
        return (
            <div className={this.props.orientation === "vertical" ? "hallway-vertical" : "hallway-horizontal"}
                onMouseDown={this.handleEvent} onMouseUp={this.handleEvent} >
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