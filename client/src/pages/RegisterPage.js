import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios';

export default function OurSignUpPage() {
    const [loggedIn, setLoggedIn] = useState(false);
    const [username, setUsername] = useState('');
    const [userId, setUserID] = useState('');
    const [password, setPassword] = useState('');    
    const [email, setEmail] = useState('');    

    const handleAddUser = () => {
        axios.get('/add_user', {username: username, userId: userId, password: password})
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

    return (
        <div>
            {!loggedIn && (
            <div className="text-center m-5-auto">
                <h2>Join us!</h2>
                <h5>Create your own personal account</h5>
                <form action="/home">
                    <p>
                        <label>Username</label><br/>
                        <input type="text" name="first_name" value = {username} onChange = {e => setUsername(e.target.value)}  required />
                    </p>
                    <p>
                        <label>UserId</label><br/>
                        <input type="text" name="user_id"  value = {userId} onChange = {e => setUserID(e.target.value)}required />
                    </p>
                    <p>
                        <label>Email address</label><br/>
                        <input type="email" name="email" value = {email} onChange = {e => setEmail(e.target.value)} required />
                    </p>
                    <p>
                        <label>Password</label><br/>
                        <input type="password" name="password" value = {password} onChange = {e => setPassword(e.target.value)}requiredc />
                    </p>
                    <p>
                        <input type="checkbox" name="checkbox" id="checkbox" required /> <span>I agree all statements in <a href="https://google.com" target="_blank" rel="noopener noreferrer">terms of service</a></span>.
                    </p>
                    <p>
                        <button id="sub_btn" onClick={handleAddUser}>Register</button>
                    </p>
                </form>
                <footer>
                    <p><Link to="/">Back to Homepage</Link>.</p>
                </footer>
            </div>
        )}
        {loggedIn}  {/* Brings it to next page */}
    </div>
    );
}