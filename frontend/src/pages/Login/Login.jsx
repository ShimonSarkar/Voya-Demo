import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";

const Login = () => {
    const navigate = useNavigate();

    useEffect(() => {
        const params = new URLSearchParams(window.location.search);
        const code = params.get("code");

        if (code) {
            handleGoogleCallback(code);
        }
    }, []);

    const handleGoogleCallback = async (code) => {
        try {
            const response = await fetch(`http://localhost:5001/auth/callback?code=${code}`);
            if (!response.ok) {
                throw new Error("Failed to authenticate with Google.");
            }

            const { jwt_token, ...userDetails } = await response.json();

            if (jwt_token) {
                localStorage.setItem("jwt", jwt_token);
                localStorage.setItem("user_data", JSON.stringify(userDetails));

                console.log("Login successful!");
                navigate("/");
            } else {
                console.log("Failed to log in. Please try again.");
            }
        } catch (error) {
            console.error("Error during Google login callback:", error);
            console.log("An error occurred during login. Please try again.");
        }
    };

    const handleGoogleLogin = async () => {
        try {
            const response = await fetch(`http://localhost:5001/auth/login`);
            const data = await response.json();
            if (data.redirect_url) {
                window.location.href = data.redirect_url;
            } else {
                console.log("Failed to initiate Google login.");
            }
        } catch (error) {
            console.error("Error during Google login:", error);
            console.log("An error occurred. Please try again.");
        }
    };

    return (
        <div className="login-container">
            {/* Branding Section */}
            <div className="branding-section">
                <h1 className="branding-title">Welcome to <span>Voya</span></h1>
                <p className="branding-motto">Streamlining corporate travel for modern businesses.</p>
            </div>

            {/* Login Section */}
            <div className="login-section">
                <div className="login-buttons">
                    <h2>Your Journey Starts Here</h2>
                    <button className="login-button" onClick={handleGoogleLogin}>
                        Login
                    </button>
                    <button className="signup-button" onClick={handleGoogleLogin}>
                        Sign Up
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Login;
