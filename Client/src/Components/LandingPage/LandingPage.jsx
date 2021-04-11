import React from 'react';
import {
    Link,
} from "react-router-dom";
import Button from 'react-bootstrap/Button';
import RTTLogo from '../../Images/RTTLogo.png';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./LandingPage.css"

export class LandingPage extends React.Component {
    render() {
        return (
            <center>
                <div id="landingPageContainer" className="container">
                    <div className="row">
                        <div className="col">
                            <h1 className="title">
                                ClueLite
                            </h1>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col text-center">
                            <Link to="/lobby" style={{ textDecoration: 'none' }} >
                                <Button variant="success" className="startButton justify-content-center">
                                    <p className="startText">Play</p>
                                </Button>
                            </Link>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col">
                            <img src={RTTLogo} style={{ width: "300px" }} alt="Runtime Terror Logo - An armored scarab beetle." />
                        </div>
                    </div>
                </div>
            </center>
        )
    }
}
export default LandingPage;