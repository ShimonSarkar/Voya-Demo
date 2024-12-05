import React from "react";
import { useNavigate } from "react-router-dom";
import "./Navbar.css";

const Navbar = () => {
    const navigate = useNavigate();

    // Check if user is logged in
    const jwt = localStorage.getItem("jwt");

    const handleNavigation = (path) => {
        navigate(path);
    };

    return (
        <>
            <nav className="navbar">
                {/* Left section: Brand */}
                <div className="navbar-brand" onClick={() => handleNavigation("/")}>
                    <h1>Voya</h1>
                </div>

                {/* Center section: Navigation Links */}
                <div className="navbar-center">
                    <button
                        className="navbar-link"
                        onClick={() => handleNavigation("/")}
                    >
                        Dashboard
                    </button>
                    <button
                        className="navbar-link"
                        onClick={() => handleNavigation("/trip")}
                    >
                        Trips
                    </button>
                    <button
                        className="navbar-link"
                        onClick={() => handleNavigation("/faq")}
                    >
                        Reimbursement
                    </button>
                    <button
                        className="navbar-link"
                        onClick={() => handleNavigation("/contact")}
                    >
                        Company Policy
                    </button>
                </div>

                {/* Right section: Icons */}
                <div className="navbar-icons">
                    {jwt ? (
                        <button
                            className="navbar-link navbar-login-button"
                            onClick={() => {
                                localStorage.clear();
                                handleNavigation("/login");
                            }}
                        >
                            Logout
                        </button>
                    ) : (
                        <button
                            className="navbar-link navbar-login-button"
                            onClick={() => {
                                localStorage.clear();
                                handleNavigation("/login");
                            }}
                        >
                            Login
                        </button>
                    )}
                </div>
            </nav>
        </>
    );
};

export default Navbar;
