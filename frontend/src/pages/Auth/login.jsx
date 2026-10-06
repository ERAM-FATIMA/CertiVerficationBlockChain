import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../../assets/styles.css";
import { useAuth } from "../../context/AuthContext";
import Navbar from "../../components/Navbar";
import api from "../../api/client"; // 👈 make sure path is correct

function Login() {
  const navigate = useNavigate();
  const [role, setRole] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const { login, getDashboardRoute } = useAuth();
  const handleLogin = async (e) => {
    e.preventDefault();

    if (!role) {
      setErrorMsg("Please select a role");
      return;
    }

    try {
      const res = await api.post(`/${role}/login`, {
        email, // or student_id depending on backend
        password,
      });

      const data = res.data;

      console.log("LOGIN RESPONSE:", data);

      const token = data.access_token || data.token;

      if (!token) {
        setErrorMsg("Invalid response from server");
        return;
      }

      login(token, role);

      navigate(getDashboardRoute(role));

    } catch (err) {
      console.error("FULL ERROR:", err);

      if (err.response) {
        console.log("BACKEND ERROR:", err.response.data);

        setErrorMsg(
          err.response.data.detail ||
          err.response.data.msg ||
          JSON.stringify(err.response.data)
        );
      } else {
        setErrorMsg("Server error. Try again later.");
      }
    }
  };

  return (
    <div className="page-bg login-page">
      <Navbar />
      <div className="page-content login-bg">
        <div className="login-card card">
          <h2>Login</h2>
          <p>Access your CertiVeri account</p>

          <form onSubmit={handleLogin}>
            <label htmlFor="role">Select Role</label>
            <select
              id="role"
              value={role}
              onChange={(e) => setRole(e.target.value)}
              className="input"
              required
            >
              <option value="">Choose Role</option>
              <option value="university">University</option>
              <option value="student">Student</option>
              <option value="employer">Employer</option>
            </select>

            <label htmlFor="email">Email</label>
            <input
              type="text"
              id="email"
              className="input"
              placeholder="Enter Email or Student ID"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              className="input"
              placeholder="Enter password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

            {errorMsg && <p className="error-msg">{errorMsg}</p>}

            <button type="submit" className="button login-button">
              Login
            </button>
          </form>

          <p className="switch-text">
            New organization? <a href="/register">Register</a>
          </p>

          <p className="info-text">
            Students are registered by universities.
            Universities issue certificates whose cryptographic hashes are stored on blockchain.
          </p>
        </div>
      </div>
    </div>
  );
}

export default Login;