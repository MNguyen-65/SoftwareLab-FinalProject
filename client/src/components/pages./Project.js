import React from "react";
import Checkout from "./Checkout";
import './UserPortal.css'
import axios from "axios";
import { useState } from "react";

export default function Project() {
  const [projectName, setProjectName] = useState('');
  const [projectId, setProjectId] = useState('');
  const [description, setDescription] = useState('');
  const [userId, setUserId] = useState('');

  const [loggedOut, setLoggedOut] = useState(false);
  const users = []
  const sets = "";


    const handleUsers = () => {
      axios.post('/get_user_projects', {userId: userId})
          .then(res => {
              if(res.data.success) {
                  alert(res.data.message);
              } else {
                  alert(res.data.message);
              }
          })
          .catch(err => {
              console.log(err);
          }
      );
  }

  const handleHWsets = () => {
    axios.post('/create_project', {userId: userId, projectName: projectName, projectId: projectId, description: description})
        .then(res => {
            if(res.data.success) {
                alert(res.data.message);
            } else {
                alert(res.data.message);
            }
        })
        .catch(err => {
            console.log(err);
        }
    );
}




    return (
   
      <div className="Project">
          <h3>Project: </h3>
          <div>
              Users in this Project:
              <ul>
              </ul>
              Hardware Sets:
              <ul>
              </ul>
              CheckIn/CheckOut Hardware:
                    <Checkout />
          </div>    
      </div>
    );
       
}