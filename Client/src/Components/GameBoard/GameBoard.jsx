import React from 'react';
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./GameBoard.css"

import HorizontalHallway from '../../Images/horizontal_hallway.png';
import VerticalHallway from '../../Images/vertical_hallway.png'
import PlayerBlue from '../../Images/player-blue.png';
import PlayerGreen from '../../Images/player-green.png';
import PlayerOrange from '../../Images/player-orange.png';
import PlayerYellow from '../../Images/player-yellow.png';
import Room from '../../Components/Room/Room'
import Hallway from '../../Components/Hallway/Hallway'

export class GameBoard extends React.Component {
    render() {
        return (
            <div className="container" >
                <div className="row" style={{ justifyContent: 'space-between' }}>
                    <div className="col-md-2">
                        <Room />
                    </div>
                    <div className="col-md-2">
                        <Hallway orientation="horizontal" />
                    </div>
                    <div className="col-md-2">
                        <Room />
                    </div>
                    <div className="col-md-2">
                        <Hallway orientation="horizontal" />
                    </div>
                    <div className="col-md-2">
                        <Room />
                    </div>
                </div>
                <div className="row" style={{ justifyContent: 'space-between' }}>
                    <div className="col-md-3">
                        <Hallway orientation="vertical" />
                    </div>
                    <div className="col-md-3">
                        <Hallway orientation="vertical" />
                    </div>
                    <div className="col-md-3">
                        <Hallway orientation="vertical" />
                    </div>
                </div>
                <div className="row" style={{ justifyContent: 'space-between' }}>

                    <div className="col-md-2">
                        <Room />
                    </div>
                    <div className="col-md-2">
                        <Hallway orientation="horizontal" />
                    </div>
                    <div className="col-md-2">
                        <Room />
                    </div>
                    <div className="col-md-2">
                        <Hallway orientation="horizontal" />
                    </div>
                    <div className="col-md-2">
                        <Room />
                    </div>
                </div>
                <div className="row" style={{ justifyContent: 'space-between' }}>
                    <div className="col-md-3">
                        <Hallway orientation="vertical" />
                    </div>
                    <div className="col-md-3">
                        <Hallway orientation="vertical" />
                    </div>
                    <div className="col-md-3">
                        <Hallway orientation="vertical" />
                    </div>
                </div>
                <div className="row" style={{ justifyContent: 'space-between' }}>
                    <div className="col-md-2">
                        <Room />
                    </div>
                    <div className="col-md-2">
                        <Hallway orientation="horizontal" />
                    </div>
                    <div className="col-md-2">
                        <Room />
                    </div>
                    <div className="col-md-2">
                        <Hallway orientation="horizontal" />
                    </div>
                    <div className="col-md-2">
                        <Room />
                    </div>
                </div>
            </div >
        )
    }
}
export default GameBoard;