import React, { useState } from 'react'
import { useLocation, Navigate } from 'react-router-dom'
import axios from 'axios'
import Select from '@mui/material/Select'
import MenuItem from '@mui/material/MenuItem'
import { FormControl, InputLabel } from '@mui/material'

//import Project from '../components/Project'

export default function ProjectsPage() {
    const [projectName, setProjectName] = useState('');
    const [currentProj, setCurrentProj] = useState('');
    const [projectId, setProjectId] = useState('');
    const [description, setDescription] = useState('');
    const [infoGot, setInfoGot] = useState(false);
    const [loggedOut, setLoggedOut] = useState(false);

    const [hwSet, setHwSet] = useState('');
    const [qty, setQty] = useState('');
    const [avail, setAvail] = useState('');
    const [cap, setCap] = useState('');

    const [projUsers, setProjUsers] = useState([]);
    const [projName, setProjName] = useState('');
    const [projDesc, setProjDesc] = useState('');
    const [projHWsets, setProjHWsets] = useState('');


    const location = useLocation();
    const searchParams = new URLSearchParams(location.search);
    const userId = searchParams.get('userId') || 'No user ID';
    const [userProjectsList, setUserProjectsList] = useState([]);
    const [hwNames, setHwNames] = useState([]);

    const [existingProjectId, setExistingProjectId] = useState('');


    const getUserProjectsList = () => {
        axios.post('/get_user_projects_list', {userId: userId})
            .then(res => {
                setUserProjectsList(res.data.projects);
            });
    }


    const getProject = (e) => {
        setExistingProjectId(e.target.value)
        axios.post('/get_project_info', {projectId: e.target.value})
            .then(res => {
                setProjName(res.data.projectName)
                setProjDesc(res.data.description)
                setProjUsers(res.data.users)
                setProjHWsets(res.data.hwSets)
            });
    }


    const getAllHwNames = () => {
        axios.post('/get_all_hw_names')
            .then(res => {
                setHwNames(res.data.hwNames)
            });
    }


    const getHwInfo = (e) => {
        setHwSet(e.target.value)
        axios.post('/get_hw_info', {hwName: e.target.value})
            .then(res => {
                setAvail(res.data.availability);
                setCap(res.data.capacity);
            })
    }

    
    const handleCheckIn = () => {
        axios.post('/check_in', {projectId: existingProjectId, hwSetName: hwSet, qty: qty, userId: userId})
            .then(res => {
                if(res.data.success) {
                    alert(res.data.message);
                    setAvail(res.data.avail)
                    setCap(res.data.cap)
                } else {
                    alert(res.data.message);
                }
            })
            .catch(err => {
                console.log(err);
            }
        );
    }

    const handleCheckOut = () => {
        axios.post('/check_out', {projectId: existingProjectId, hwSetName: hwSet, qty: qty, userId: userId})
            .then(res => {
                if(res.data.success) {
                    alert(res.data.message);
                    setAvail(res.data.avail)
                    setCap(res.data.cap)
                } else {
                    alert(res.data.message);
                }
            })
            .catch(err => {
                console.log(err);
            }
        );
    }


    const handleCreateProject = () => {
        axios.post('/create_project', {userId: userId, projectName: projectName, projectId: projectId, description: description})
            .then(res => {
                if(res.data.success) {
                    alert(res.data.message);
                    getUserProjectsList();
                } else {
                    alert(res.data.message);
                }
            })
            .catch(err => {
                console.log(err);
            }
        );
    }


    const renderProjectMenu = (projects) => {
        return projects.map(project => <MenuItem value = {project}>{project}</MenuItem>)
    }
    
    const renderHWMenu = (hwsets) => {
        return hwsets.map(hw => <MenuItem value = {hw}>{hw}</MenuItem>)
    }
    
    
    const handleJoinProject = () => {
        axios.post('/join_project', {userId: userId, projectId: existingProjectId})
            .then(res => {
                if(res.data.success) {
                    alert(res.data.message);
                    getUserProjectsList();
                } else {
                    alert(res.data.message);
                }
            })
            .catch(err => {
                console.log(err);
            }
        );
    };

    const handleLogout = () => {
        setLoggedOut(true);
    }

    if (loggedOut) {
        return <Navigate to={'/'} replace/>;
    }


    if (!infoGot) {
        getUserProjectsList();
        getAllHwNames();
        setInfoGot(true)
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
            <h2>Check out or Check in hardware for project</h2>
                <div>
                    <label>
                        <div>
                            <FormControl >
                                <InputLabel id = "proj-list">Project id</InputLabel>
                                <Select 
                                    labelId='proj-list'
                                    value={existingProjectId}
                                    label='Choose Project Id' 
                                    sx={{width: 150}}
                                    onChange={e => getProject(e)} 
                                >
                                    {renderProjectMenu(userProjectsList)}

                                </Select>
                                {/* {currentProj} */}
                            </FormControl>                                
                            <div>
                                Project Name: {projName}
                                </div>
                                <div>
                                Project id: {existingProjectId}
                                </div>
                                <div>
                                Project Description: {projDesc}
                                </div>
                                <div>
                                Users: {projUsers}
                                </div>        
                            <div>
                            <FormControl >
                                <InputLabel id = "hard-list">Hardware Set</InputLabel>
                                <Select 
                                    labelId='hard-list'
                                    value={hwSet}
                                    label='Choose Hardware Set' 
                                    sx={{width: 150}}
                                    onChange={e => getHwInfo(e)} 
                                >
                                    {renderHWMenu(hwNames)}
                                </Select>
                            </FormControl>
                            </div>
                        <div>   
                            Availability: {avail}
                        </div>
                        <div>   
                            Capacity: {cap} 
                        </div>
                        </div>
                        <br />
                        Enter Quantity of Hardware:
                        <div>
                            <input type="text" placeholder="Quantity" value={qty} onChange={e => setQty(e.target.value)} />
                        </div>
                    </label>
                    <input type="submit" value="Check In" onClick={handleCheckIn}/>
                    <input type="submit" value="Check Out" onClick={handleCheckOut}/>
                </div>
            {/* </form> */}
        </div>
    )
}