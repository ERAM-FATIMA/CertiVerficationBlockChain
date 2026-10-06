import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../../assets/styles.css";
import Navbar from "../../components/Navbar";
import api from "../../api/client"; // 👈 make sure path is correct

function Register() {
  const navigate = useNavigate();

  const [role, setRole] = useState("");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();

    if (!role) {
      setErrorMsg("Please select a role");
      return;
    }

    try {
      const res = await api.post(`/${role}/register`, {
        name,
        email,
        password,
      });

      const data = res.data;

      setSuccessMsg("Registration successful! Redirecting to login...");
      setErrorMsg("");

      setTimeout(() => navigate("/login"), 2000);

    } catch (err) {
      console.error(err);

      if (err.response) {
        setErrorMsg(
          err.response.data.detail ||
          err.response.data.msg ||
          "Registration failed"
        );
      } else {
        setErrorMsg("Server error. Try again later.");
      }

      setSuccessMsg("");
    }
  };

  return (
    <div className="page-bg login-page">
      <Navbar />
      <div className="page-content login-bg">
        <div className="login-card card">
          <h2>Register</h2>
          <p>Create your CertiVeri account</p>

          <form onSubmit={handleRegister}>
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
              <option value="employer">Employer</option>
            </select>

            <label htmlFor="name">Name</label>
            <input
              type="text"
              id="name"
              className="input"
              placeholder="Enter Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />

            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              className="input"
              placeholder="Enter Email"
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
            {successMsg && <p className="success-msg">{successMsg}</p>}

            <button type="submit" className="button login-button">
              Register
            </button>
          </form>

          <p className="switch-text">
            Already registered? <a href="/login">Login</a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Register;