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
        if(this.state.available <= 0) {

        }

        if(this.state.available <= this.state.total) {

        }

        else {
            this.setState({available: this.state.available + 1})
            this.setState({used: this.state.total - this.state.available - 1})
        }
    };

    incrementUsed = () => {
        if(this.state.used >= this.state.total) {

        }
        
        else {
            this.setState({used: this.state.used + 1})
            this.setState({available: this.state.available - 1})
        }
    }

    render () {
        return (
            <div>
            <p> Welcome to the server checkout! </p>
            <Box sx={{ display: 'flex', flexDirection: 'column'}}>
            <Box sx={{ display: 'flex', mb: 2, border: '10px solid #33FFF9' }}>
            <Box sx={{  display: 'flex', alignItems: 'center', mt: 0 }}>   
            <span ststyle={{ textAlign: 'left' }}> <b> {this.state.total} </b> </span> &nbsp;&nbsp;
            <p>  Total Servers <b> | </b> </p>  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <span> <b> {this.state.available} </b> </span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <p> Available Servers </p> &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <button type="submit" onClick={this.incrementAvailable} style={{ backgroundColor: '#71FF33', border: 'none', color: 'black', padding: '10px', borderRadius: '5px' }}>
              Check In Server From Deployment
            </button> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;
            <p> <b> | </b> </p> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;
            <span> <b> {this.state.used} </b> </span> &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;
            <p> Servers Under Deployment </p> &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;
            <button type="submit" onClick={this.incrementAvailable} style={{ backgroundColor: '#71FF33', border: 'none', color: 'black', padding: '10px', borderRadius: '5px' }}>
            Check Out Server From Deployment 
            </button> &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;
            </Box>
            </Box>
            </Box>
      </div>
        );
    }
}

export default Counter;

