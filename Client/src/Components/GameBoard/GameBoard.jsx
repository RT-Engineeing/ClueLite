import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './GameBoard.css'

import Room from '../../Components/Room/Room'
import Hallway from '../../Components/Hallway/Hallway'

import { rooms } from '../../Cards/Cards'

export class GameBoard extends React.Component {
    render() {
        return (
            <div className='container' id="boardContainer"  >
                <div className='row' style={{ justifyContent: 'space-between' }}>
                    <div className='col-md-2' >
                        <Room x='0' y='0' name={rooms[0]} gameState={this.props.gameState()} />
                    </div>
                    <div className='col-md-2'>
                        <Hallway orientation='horizontal' x='1' y='0' gameState={this.props.gameState()} />
                    </div>
                    <div className='col-md-2'>
                        <Room x='2' y='0' name={rooms[1]} gameState={this.props.gameState()} />
                    </div>
                    <div className='col-md-2'>
                        <Hallway orientation='horizontal' x='3' y='0' gameState={this.props.gameState()} />
                    </div>
                    <div className='col-md-2'>
                        <Room x='4' y='0' name={rooms[2]} gameState={this.props.gameState()} />
                    </div>
                </div>
                <div className='row' style={{ justifyContent: 'space-between' }}>
                    <div className='col-md-3'>
                        <Hallway orientation='vertical' x='0' y='1' gameState={this.props.gameState()} />
                    </div>
                    <div className='col-md-3'>
                        <Hallway orientation='vertical' x='1' y='1' gameState={this.props.gameState()} />
                    </div>
                    <div className='col-md-3'>
                        <Hallway orientation='vertical' x='2' y='1' gameState={this.props.gameState()} />
                    </div>
                </div>
                <div className='row' style={{ justifyContent: 'space-between' }}>

                    <div className='col-md-2'>
                        <Room x='0' y='2' name={rooms[3]} gameState={this.props.gameState()} />
                    </div>
                    <div className='col-md-2'>
                        <Hallway orientation='horizontal' x='1' y='2' gameState={this.props.gameState()} />
                    </div>
                    <div className='col-md-2'>
                        <Room x='2' y='2' name={rooms[4]} gameState={this.props.gameState()} />
                    </div>
                    <div className='col-md-2'>
                        <Hallway orientation='horizontal' x='3' y='2' gameState={this.props.gameState()} />
                    </div>
                    <div className='col-md-2'>
                        <Room x='4' y='2' name={rooms[5]} gameState={this.props.gameState()} />
                    </div>
                </div>
                <div className='row' style={{ justifyContent: 'space-between' }}>
                    <div className='col-md-3'>
                        <Hallway orientation='vertical' x='0' y='3' gameState={this.props.gameState()} />
                    </div>
                    <div className='col-md-3'>
                        <Hallway orientation='vertical' x='1' y='3' gameState={this.props.gameState()} />
                    </div>
                    <div className='col-md-3'>
                        <Hallway orientation='vertical' x='2' y='3' gameState={this.props.gameState()} />
                    </div>
                </div>
                <div className='row' style={{ justifyContent: 'space-between' }}>
                    <div className='col-md-2'>
                        <Room x='0' y='4' name={rooms[6]} gameState={this.props.gameState()} />
                    </div>
                    <div className='col-md-2'>
                        <Hallway orientation='horizontal' x='1' y='4' gameState={this.props.gameState()} />
                    </div>
                    <div className='col-md-2'>
                        <Room x='2' y='4' name={rooms[7]} gameState={this.props.gameState()} />
                    </div>
                    <div className='col-md-2'>
                        <Hallway orientation='horizontal' x='3' y='4' gameState={this.props.gameState()} />
                    </div>
                    <div className='col-md-2'>
                        <Room x='4' y='4' name={rooms[8]} gameState={this.props.gameState()} />
                    </div>
                </div>
            </div >
        )
    }
}
export default GameBoard;