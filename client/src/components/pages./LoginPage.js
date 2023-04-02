import React from 'react'
import { Link } from 'react-router-dom'
import './LoginPage.css'

export default function SignInPage() {
    return (
        <div className="text-center m-5-auto" id="loginlanding">
            <h2 id="loginsign">Sign in to us</h2>
            <form action="/home" className="login-form"> 
                <p className="text-center">
                    <label style={{ color: 'red', textAlign: 'center', fontFamily: 'Arial, Helvetica, sans-serif'}}>Username or email address</label><br/>
                    <input style={{textAlign: 'center'}} type="text" name="first_name" required />
                </p>
                <p>
                    <label style={{ color: 'red', textAlign: 'center', fontFamily: 'Arial, Helvetica, sans-serif'}}> Password</label>
                    <br/>
                    <input type="password" name="password" required />
                </p>
                <p>
                    <button id="sub_btn" type="submit">Login</button>
                </p>
            </form>
            <footer>
                <p id="linkedpageheader">First time? </p>
                <p id="linkedpage" style={{fontFamily: 'Arial, Helvetica, sans-serif', color: 'lightgreen'}}> <Link to="/register" style={{color: 'rgb(51, 205, 51)'}}>Create an account</Link></p>
                <p id="linkedpage" style={{fontFamily: 'Arial, Helvetica, sans-serif', color: 'lightgreen'}}><Link to="/" style={{color: 'rgb(51, 205, 51)'}}>Back to Homepage</Link>.</p>
                <p id="linkedpage" style={{fontFamily: 'Arial, Helvetica, sans-serif', color: 'lightgreen'}}><Link to="/forget-password" style={{color: 'rgb(51, 205, 51)'}}> Forget password?</Link></p>
            </footer>
        </div>
    )
}

