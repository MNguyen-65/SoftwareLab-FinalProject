import React from "react";
import Checkout from "./Checkout";
import './UserPortal.css'

class Project extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        id: ''
      };
    }

    render() {
      return (
        <div className="Project">
            <h3>Project: {this.state.id}</h3>
            <div>
                Users in this Project:
                <ul>
                </ul>
                Hardware Sets:
                <ul>
                </ul>
                CheckIn/CheckOut Hardware:
                      <Checkout />   
\            </div>    
        </div>
      );
    }
   }

   export default Project;