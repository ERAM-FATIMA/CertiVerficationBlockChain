import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

function DashboardLayout({ title, children }) {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="dashboard-container">

      {/* TOPBAR */}
      <header className="topbar">
        <h2>{title}</h2>

        <div style={{ display: "flex", gap: "10px" }}>
          <button className="logout-btn" onClick={() => navigate("/")}>
            Home
          </button>

          <button onClick={handleLogout} className="logout-btn">
            Logout
          </button>
        </div>
      </header>

      {/* CONTENT */}
      <div className="main-content">
        {children}
      </div>

    </div>
  );
}

export default DashboardLayout;