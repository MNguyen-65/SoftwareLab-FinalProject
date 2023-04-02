import React, { useState } from 'react'
import { useNavigate, Navigate, Link } from 'react-router-dom'
import axios from 'axios';
import UserPortal from './UserPortal'

export default function OurSignUpPage() {
    const [loggedIn, setLoggedIn] = useState(false);
    const [username, setUsername] = useState('');
    const [userId, setUserID] = useState('');
    const [password, setPassword] = useState('');    
    const [email, setEmail] = useState('');    

    

    const handleAddUser = (e) => {
        e.preventDefault();

        axios.post('/add_user', {username: username, userId: userId, password: password})
            .then(res => {
                if (res.data.success) {
                    setLoggedIn(true);
                } else {
                    alert(res.data.message);
                }
            })
            .catch(err => {
                console.log(err);
            });
      };

    if (loggedIn) {
        return <Navigate to={`/main?userId=${userId}`} replace/>;
    }

    return (
        <div>
            {!loggedIn && (
            <div className="text-center m-5-auto" style={{textAlign: "center", color: 'red'}}>
                <h2 id = "hello" style={{textAlign: "center", color: 'green'}}>Join us!</h2>
                <h5 id = "hello" style={{textAlign: "center", color: 'green'}}>Create your own personal account</h5>
                <form action="/main"> 
                    <p>
                        <label>Username</label><br/>
                        <input type="text" name="first_name" value = {username} onChange = {e => setUsername(e.target.value)}  required />
                    </p>
                    <p>
                        <label>UserId</label><br/>
                        <input type="text" name="user_id"  value = {userId} onChange = {e => setUserID(e.target.value)}required />
                    </p>
                    {/* <p>
                        <label>Email address</label><br/>
                        <input type="email" name="email" value = {email} onChange = {e => setEmail(e.target.value)} required />
                    </p> */}
                    <p>
                        <label>Password</label><br/>
                        <input type="password" name="password" value = {password} onChange = {e => setPassword(e.target.value)}requiredc />
                    </p>
                    {/* <p>
                        <input type="checkbox" name="checkbox" id="checkbox" required /> <span>I agree all statements in <a href="https://google.com" target="_blank" rel="noopener noreferrer">terms of service</a></span>.
                    </p> */}
                    <p>
                        <button id="sub_btn" onClick={handleAddUser}>Register</button>
                    </p>
                </form>
                <footer>
                    <p><Link to="/" style={{textAlign: "center", color: 'orange'}}>Back to Homepage</Link>.</p>
                </footer>
            </div>
        )}
        {loggedIn &&(
            <div>
                <h2>Hard-coding the below in LoginPage.js but it should be through app</h2>
                <UserPortal />
            </div>
            )}
    </div>
    );
}