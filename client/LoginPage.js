import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'

import '../../App.css'

export default function SignInPage() {
    const [user, setUser] = useState('')
    const [pass, setPass] = useState('')
    const [success, setSuccess] = useState('')


    const handleLogin = () => {
        axios.post('/login', {username: user, password: pass})
          .then(res => {
            if (res.data.success) {
              setSuccess(true);
            } else {
              alert('Login failed. Please try again.');
            }
          })
          .catch(err => {
            console.log(err);
          });
      };
    
    
      const handleAddUser = () => {
        axios.post('/add_user', {user: user, pass: pass})
          .then(res => {
            if (res.data.success) {
              setSuccess(true);
            } else {
              alert('Account creation failed. Please try again.');
            }
          })
          .catch(err => {
            console.log(err);
          });
      };
    

    return (
        <div className="text-center m-5-auto">
            <h2>Sign in to us</h2>
            <form action="/home" >
                <p>
                    <label>Username or email address</label><br/>
                    <input type="text" name="first_name" value = {user}
                     onChange = { e => setUser(e.target.value) } required />

                </p>
                <p>
                    <label>Password</label>
                    <Link to="/forget-password"><label className="right-label">Forget password?</label></Link>
                    <br/>
                    <input type="password" name="password" value = {pass}
                     onChange = { e => setPass(e.target.value) } required />
                </p>
                <p>
                    <button id="sub_btn" onClick = {handleLogin} type="submit">Login</button>
                   
                </p>
            </form>
            <footer>
                <p>First time? <Link to="/register">Create an account</Link>.</p>
                <p><Link to="/">Back to Homepage</Link>.</p>
            </footer>
        </div>
    )
}
