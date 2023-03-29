import React, { useState } from 'react'
import { useLocation, Link } from 'react-router-dom'
import axios from 'axios'

import Project from '../components/Project'

export default function ProjectsPage() {
    const [userId, setUserId] = useState('');
    const [projectName, setProjectName] = useState('');
    const [projectId, setProjectId] = useState('');
    const [description, setDescription] = useState('');

    const location = useLocation();

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
    
    
    const handleJoinProject = () => {
        axios.get('/join_project', {userId: userId, projectId: existingProjectId})
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
        <div className="text-center m-5-auto">
            <h2>Welcome!</h2>
            <p>User ID: </p>
            {/* <form action="/projenter"> */}
                <p>
                    <label>Create Project</label>
                    <input type="text" placeholder="Project Name" value={projectName} onChange={e => setProjectName(e.target.value)} />
                    <br />
                    <input type="text" placeholder="Project ID" value={projectId} onChange={e => setProjectId(e.target.value)} />
                    <br />
                    <input type="text" placeholder="Description" value={description} onChange={e => setDescription(e.target.value)} />
                    <br />
                    <button onClick={handleCreateProject}>Create Project</button>
                </p>
                <p>
                    <label>Join Project</label>
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