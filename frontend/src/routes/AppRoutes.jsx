import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "../components/Navbar/Navbar";
import Dashboard from "../pages/Dashboard/Dashboard";
import Trip from "../pages/Trip/Trip";
import Login from "../pages/Login/Login";

const AppRoutes = () => {
    return (
        <Router>
            <Navbar />
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/" element={<Dashboard />} />
                <Route path="/trip" element={<Trip />} />
            </Routes>
        </Router>
    );
};

export default AppRoutes;