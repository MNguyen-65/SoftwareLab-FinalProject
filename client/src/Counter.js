import React, {Component} from 'react';
import { Box, Button, TextField } from '@mui/material';

class Counter extends Component {
        state = {
            total: 10,
            available: 10,
            used: 0
        }

    incrementTotal = () => {
        this.setState({total: this.state.total + 1})
    };

    incrementAvailable = () =>  {
        this.setState({available: this.state.available + 1})
        this.setState({used: this.state.total - this.state.available - 1})
    };

    incrementUsed = () => {
        this.setState({used: this.state.used + 1})
        this.setState({available: this.state.available - 1})
    }

    render () {
        return (
            <div>
            <Box sx={{ display: 'flex', flexDirection: 'column'}}>
            <Box sx={{ display: 'flex', mb: 2, border: '10px solid #C8E6C9' }}>
            <Box sx={{  display: 'flex', alignItems: 'center', mt: -2 }}>   
            <span ststyle={{ textAlign: 'left' }}> {this.state.total} </span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
            <p> Total Number of Servers | </p>  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <span> {this.state.available} </span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <p> Available Servers </p> &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <button type="submit" onClick={this.incrementAvailable}> Check Out Server  </button> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <p> | </p> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;
            <span> {this.state.used} </span> &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;
            <p> Servers Under Deployment </p> &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;
            <button type="submit" onClick={this.incrementUsed}> Check In Server </button> &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;
            </Box>
            </Box>
            </Box>
      </div>
        );
    }
}

export default Counter;

