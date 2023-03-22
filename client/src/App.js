import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

import LoginPage from './components/pages/LoginPage'

import './App.css'

export default function App() {
    return (
        <Router>
                <Routes>
                    <Route path="/" element={<LoginPage /> } />
                </Routes>
        </Router>
    )
}

