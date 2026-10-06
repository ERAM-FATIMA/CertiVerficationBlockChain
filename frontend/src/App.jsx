import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Auth/login";
import Register from "./pages/Auth/register";
import StudentDashboard from "./pages/Dashboard/StudentDashboard";
import UniversityDashboard from "./pages/Dashboard/UniversityDashboard";
import EmployerDashboard from "./pages/Dashboard/EmployerDashboard";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* PUBLIC */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* PROTECTED */}
        <Route
          path="/dashboard/student"
          element={
            <ProtectedRoute allowedRole="student">
              <StudentDashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/dashboard/university"
          element={
            <ProtectedRoute allowedRole="university">
              <UniversityDashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/dashboard/employer"
          element={
            <ProtectedRoute allowedRole="employer">
              <EmployerDashboard />
            </ProtectedRoute>
          }
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;