import React from 'react'
import { Link } from 'react-router-dom'


export default function ForgetPasswordPage() {
    return (
        <div className="text-center m-5-auto" id='forgotlanding'  style={{textAlign: "center", color: 'red'}}>
            <h2 id='reset' style={{textAlign: "center", color: 'green'}}>Reset your password</h2>
            <h5 id='reset' style={{textAlign: "center", color: 'green'}}>Enter your email address and we will send you a new password</h5>
            <form action="/login">
                <p>
                    <label id="reset_pass_lbl" >Email address</label><br/>
                    <input type="email" name="email" required />
                </p>
                <p>
                    <button id="sub_btn" type="submit">Send password reset email</button>
                </p>
            </form>
            <footer>
                <p style={{textAlign: "center", color: 'orange'}}>First time? <Link to="/register" style={{textAlign: "center", color: 'orange'}}>Create an account</Link>.</p>
                <p style={{textAlign: "center", color: 'orange'}}><Link to="/" style={{textAlign: "center", color: 'orange'}}>Back to Homepage</Link>.</p>
            </footer>
        </div>
    )
}