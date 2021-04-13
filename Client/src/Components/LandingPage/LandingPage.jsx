import React from 'react';
import {
    Link,
} from "react-router-dom";
import Button from 'react-bootstrap/Button';
import RTTLogo from '../../Images/RTTLogo.png';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./LandingPage.css"
import axios from 'axios';

export class LandingPage extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            sessionKey: undefined,
            playerName: undefined,
        }
    }

    render() {

        const playButton = (
            <Button variant="success" className="startButton justify-content-center">
                <p className="startText">Play</p>
            </Button>
        );

        const loadingButton = (
            <Button variant="success" className="loadingButton justify-content-center">
                <p className="startText">Loading...</p>
            </Button>
        );

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
                            <Link to={{
                                pathname: '/lobby',
                                state: {
                                    sessionKey: this.state.sessionKey,
                                    playername: this.state.playername
                                }
                            }} style={{ textDecoration: 'none' }}>
                                {this.state.sessionKey ? playButton : loadingButton}
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

        const playername = response.data["playername"];
        const sessionKey = response.data["sessionId"];

        // console.log("session key: " + sessionKey);
        this.setState({
            sessionKey: sessionKey,
            playername: playername
        });
        // console.log("updated state: " + this.state);

    }

}
export default LandingPage;