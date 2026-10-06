import { Link, useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Navbar() {
  const { token, role, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  // DASHBOARD LOGIC
  const handleDashboard = () => {
    if (!token) {
      alert("Please login first!");
      navigate("/");
      return;
    }

    if (role === "student") navigate("/dashboard/student");
    else if (role === "university") navigate("/dashboard/university");
    else if (role === "employer") navigate("/dashboard/employer");
  };

  return (
    <div className="navbar">
      <div
        className="logo"
        style={{ cursor: "pointer" }}
        onClick={() => navigate("/")}
      >
        CertiVeri
      </div>

      <div className="nav-actions">

        {/* 🔥 ALWAYS VISIBLE */}
        <button className="nav-btn" onClick={handleDashboard}>
          Dashboard
        </button>

        {!token ? (
          <>
            {location.pathname !== "/login" && (
              <Link to="/login" className="nav-btn">Login</Link>
            )}

            {location.pathname !== "/login" &&
              location.pathname !== "/register" && (
              <span className="nav-divider"></span>
            )}

            {location.pathname !== "/register" && (
              <Link to="/register" className="nav-btn register-btn">
                Register
              </Link>
            )}
          </>
        ) : (
          <>
            <Link to="/" className="nav-btn">Home</Link>

            <button className="nav-btn" onClick={handleLogout}>
              Logout
            </button>
          </>
        )}
      </div>
    </div>
  );
}

export default Navbar;