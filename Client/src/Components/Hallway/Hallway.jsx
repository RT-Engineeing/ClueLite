import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./Hallway.css";
import HallwayImageVertical from '../../Images/vertical_hallway.png'
import HallwayImageHorizontal from '../../Images/horizontal_hallway.png'

export class Hallway extends React.Component {

    render() {
        return (
            <div>
                <img src={this.props.orientation === "vertical" ? HallwayImageVertical : HallwayImageHorizontal} alt='Room' />
            </div>
        );
    }
}
export default Hallway;