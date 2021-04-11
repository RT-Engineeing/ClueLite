import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./GamePieceContainer.css";

export class GamePieceContainer extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            pieces: [1, 2]
        }
    }

    render() {
        return (
            <React.Fragment>
                {
                    this.state.pieces.map(piece => (
                        <React.Fragment>
                            [{piece}]
                        </React.Fragment>
                    ))
                }
            </React.Fragment>);
        ;
    }
}
export default GamePieceContainer;