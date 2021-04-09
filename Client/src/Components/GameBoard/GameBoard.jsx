import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './GameBoard.css'

// import PlayerBlue from '../../Images/player-blue.png';
// import PlayerGreen from '../../Images/player-green.png';
// import PlayerOrange from '../../Images/player-orange.png';
// import PlayerYellow from '../../Images/player-yellow.png';
import Room from '../../Components/Room/Room'
import Hallway from '../../Components/Hallway/Hallway'

export class GameBoard extends React.Component {
    render() {
        return (
            <div className='container' id="boardContainer"  >
                <div className='row' style={{ justifyContent: 'space-between' }}>
                    <div className='col-md-2' >
                        <Room x='0' y='0' name='USA' />
                    </div>
                    <div className='col-md-2'>
                        <Hallway orientation='horizontal' x='1' y='0' name='Atlantic Ocean' />
                    </div>
                    <div className='col-md-2'>
                        <Room x='2' y='0' name='Ireland' />
                    </div>
                    <div className='col-md-2'>
                        <Hallway orientation='horizontal' x='3' y='0' name='The Baltics' />
                    </div>
                    <div className='col-md-2'>
                        <Room x='4' y='0' name='Russia' />
                    </div>
                </div>
                <div className='row' style={{ justifyContent: 'space-between' }}>
                    <div className='col-md-3'>
                        <Hallway orientation='vertical' x='0' y='1' name='Florida' />
                    </div>
                    <div className='col-md-3'>
                        <Hallway orientation='vertical' x='1' y='1' name='Nigeria' />
                    </div>
                    <div className='col-md-3'>
                        <Hallway orientation='vertical' x='2' y='1' name='China' />
                    </div>
                </div>
                <div className='row' style={{ justifyContent: 'space-between' }}>

                    <div className='col-md-2'>
                        <Room x='0' y='2' name='Brazil' />
                    </div>
                    <div className='col-md-2'>
                        <Hallway orientation='horizontal' x='1' y='2' name='Atlantic Ocean' />
                    </div>
                    <div className='col-md-2'>
                        <Room x='2' y='2' name='The Congo' />
                    </div>
                    <div className='col-md-2'>
                        <Hallway orientation='horizontal' x='3' y='2' name='India' />
                    </div>
                    <div className='col-md-2'>
                        <Room x='4' y='2' name='The Phillippines' />
                    </div>
                </div>
                <div className='row' style={{ justifyContent: 'space-between' }}>
                    <div className='col-md-3'>
                        <Hallway orientation='vertical' x='0' y='3' name='Argentina' />
                    </div>
                    <div className='col-md-3'>
                        <Hallway orientation='vertical' x='1' y='3' name='South Africa' />
                    </div>
                    <div className='col-md-3'>
                        <Hallway orientation='vertical' x='2' y='3' name='Australia' />
                    </div>
                </div>
                <div className='row' style={{ justifyContent: 'space-between' }}>
                    <div className='col-md-2'>
                        <Room x='0' y='4' name='Southern Ocean 1' />
                    </div>
                    <div className='col-md-2'>
                        <Hallway orientation='horizontal' x='1' y='4' name='Southern Ocean 2' />
                    </div>
                    <div className='col-md-2'>
                        <Room x='2' y='4' name='Southern Ocean 3' />
                    </div>
                    <div className='col-md-2'>
                        <Hallway orientation='horizontal' x='3' y='4' name='Antarctica' />
                    </div>
                    <div className='col-md-2'>
                        <Room x='1' y='4' name='Penguins' />
                    </div>
                </div>
            </div >
        )
    }
}
export default GameBoard;