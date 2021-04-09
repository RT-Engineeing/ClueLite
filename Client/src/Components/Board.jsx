//import React and Square component
import React from 'react';
import { Square } from './Square';

//main board component with game logic
class Board extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            x: 0,
            y: 0,
            //this sets up an empty board
            //"+"" represenets an empty square, "b" is a black stone and "w" is a white stone
            'grid': Array(19).fill().map(x => Array(19).fill("+"))
        };
        //bind this word to helper functions
        this.handleClick = this.handleClick.bind(this);
        this.handleReset = this.handleReset.bind(this);
    }

    //generate a new empty grid and set it to the grid state with setState
    handleReset() {
        let newGrid = Array(19).fill().map(x => Array(19).fill("+"));
        this.setState({ 'grid': newGrid });
    }

    async componentWillReceiveProps(nextProps) {
        console.log(nextProps);
        this.handleClick(nextProps.x, nextProps.y);
        await this.setState({ x: nextProps.x, y: nextProps.y });

    }

    handleClick(x, y) {
        //only add a peice and check for wins if the clicked square is empty
        if (this.state.grid[x][y] === '+') {
            //we don't want to mutate state directly, so we store the reference to 'grid' in a const
            const g = this.state.grid;
            //set the grid square cooresponding to the clicked square to the color of the current player
            g[x][y] = 'w'
            //set the state with the new grid data
            this.setState({ 'grid': g, 'isWhite': !this.state.isWhite })

        }
    }
    render() {
        //define styles for the <table> element in the return() function below
        const style = {
            textAlign: "center",
            margin: "auto",
            height: "auto",
            width: "500px",
            border: "1px solid black",
            tableLayout: 'fixed',
        };
        const g = this.state.grid;
        //loop through the squares in each row and generate a new Square component,
        //passing in props to the Square component in the nested map() function
        const board = g.map((row, i) => {
            return (
                <tr key={"row_" + i}>
                    {row.map((col, j) => {
                        //set the color of the square based on state.grid
                        const color_ = g[i][j] === '+' ? '#e4e4a1' : g[i][j] === 'w' ? 'white' : 'black';
                        //return Square component, passing in the following as props:
                        //square color defined above in color_,
                        //a value for the key which React needs (I think) and
                        //a function to handle clicks with grid coordinates passed in as arguments
                        return (
                            <Square handleClick={() => this.handleClick(i, j)} color={color_} key={i + "_" + j} />
                        )
                    }
                    )
                    }
                </tr>)
        });

        //returns the board with the Square Components in {board},
        //as well as a simple Button component that takes the handleReset function as a prop
        //this could be further refactored to separate the layout and styling, but it isn't that complicated so I will leave it like this
        return (
            <div style={{ textAlign: 'center' }}>
                <div style={{ margin: 'auto', width: "40%" }}>
                    <table cellSpacing="0" style={style}>
                        <tbody>
                            {board}
                        </tbody>
                    </table>
                </div>
                <br />
            </div>
        )
    }
}
export default Board;