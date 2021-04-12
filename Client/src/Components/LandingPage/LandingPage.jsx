import React from 'react';
import {
    Link,
} from "react-router-dom";
import Button from 'react-bootstrap/Button';
import RTTLogo from '../../Images/RTTLogo.png';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./LandingPage.css"
import axios from 'axios';
import { Route, useHistory } from 'react-router';

export class LandingPage extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            canJoin: false
        }
    }

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

    async componentDidMount() {
        await this.findLobby();
    }

    async findLobby() {

        const response = await axios.get("http://localhost:5000/session");
        console.log(response.data);
        const isSessionFull = response.data["isSessionFull"];
        console.log(isSessionFull);
        if (isSessionFull === false) {
            this.setState({ canJoin: !isSessionFull });
            console.log(this.state);
        }
    }

    processSessionResponse(sessionResponse) {
        if (sessionResponse["isSessionFull"] === false) {
            console.log("open session yee haw");
        }
    }
}
export default LandingPage;