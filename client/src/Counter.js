import React, {Component} from 'react';

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
            <span> {this.state.total} </span>
            <button type="submit" onClick={this.incrementTotal}> Total Number of Servers - Will Not Change </button>
            <span> {this.state.available} </span>
            <button type="submit" onClick={this.incrementAvailable}> Servers that are available </button>
            <span> {this.state.used} </span>
            <button type="submit" onClick={this.incrementUsed}> Servers that are being used </button>
        </div>
        );
    }
}

export default Counter;