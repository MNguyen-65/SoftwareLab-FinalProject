import React, { useState } from 'react'
import { useLocation, Navigate, Link } from 'react-router-dom'
import Select from '@mui/material/Select'
import axios from 'axios'

import Project from '../components/Project'

export default function ProjectsPage() {
    const [projectName, setProjectName] = useState('');
    const [projectId, setProjectId] = useState('');
    const [description, setDescription] = useState('');
    const [loggedOut, setLoggedOut] = useState(false);

    const location = useLocation();
    const searchParams = new URLSearchParams(location.search);
    const userId = searchParams.get('userId') || 'No user ID';
    const userProjectsList = [];

    const [existingProjectId, setExistingProjectId] = useState('');


    const handleCreateProject = () => {
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
    
    
 const handleJoinProject = async () => {
    try {
      const response = await fetch(
        `/join_project?projectId=${existingProjectId}&userId=${userId}`
      );
      const data = await response.json();

      if (data.success) {
        alert('Successfully joined the project');
      } else {
        alert('Error joining the project: ' + data.message);
      }
    } catch (error) {
      alert('Error joining the project: ' + error.message);
    }
  };

    const handleLogout = () => {
        setLoggedOut(true);
    }

    if (loggedOut) {
        return <Navigate to={'/'} replace/>;
    }

    return (
        <div className="text-center m-5-auto">
            <button onClick={handleLogout}> Log off</button>
            <h1>Welcome!</h1>
            <p>User ID: {userId}</p>
            {/* <form action="/projenter"> */}
                <p>
                    <h2>Create Project</h2>
                    <input type="text" placeholder="Project Name" value={projectName} onChange={e => setProjectName(e.target.value)} />
                    <br />
                    <input type="text" placeholder="Project ID" value={projectId} onChange={e => setProjectId(e.target.value)} />
                    <br />
                    <input type="text" placeholder="Description" value={description} onChange={e => setDescription(e.target.value)} />
                    <br />
                    <button onClick={handleCreateProject}>Create Project</button>
                </p>
                <p>
                    <h2>Join Project</h2>
                    <input type="text" placeholder="Project ID" value={existingProjectId} onChange={e => setExistingProjectId(e.target.value)} />
                    <br />
                    <button onClick={handleJoinProject}>Join Project</button>
                </p>
            <h2>Your Projects</h2>
                <div>
                    <Project />
                </div>
            {/* </form> */}
        </div>
    )
}