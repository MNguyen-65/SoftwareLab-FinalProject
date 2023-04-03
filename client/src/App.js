
import React from 'react'
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom'

import LoginPage from './pages/LoginPage'
import UserPortal from './pages/UserPortal'
import RegisterPage from './pages/RegisterPage'
import ForgotPassword from './pages/ForgotPassword'

export default function App() {
    return (
        <Router>
                <Routes>
                    <Route path="/" element={<LoginPage /> } />
                    <Route path="/forgot-password" element={<ForgotPassword />} />
                    <Route path="/register" element={<RegisterPage />} />
                    <Route path="/main" element={<UserPortal />} />
                </Routes>
        </Router>
    )
}