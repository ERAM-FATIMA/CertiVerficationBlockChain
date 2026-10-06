import { createContext, useContext, useState } from "react";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem("access_token"));
  const [role, setRole] = useState(localStorage.getItem("role"));

  const getDashboardRoute = (role) => {
    if (role === "student") return "/dashboard/student";
    if (role === "university") return "/dashboard/university";
    if (role === "employer") return "/dashboard/employer";
    return "/";
  };

  const login = (token, role) => {
    localStorage.setItem("access_token", token);
    localStorage.setItem("role", role);
    setToken(token);
    setRole(role);
  };

  const logout = () => {
    localStorage.clear();
    setToken(null);
    setRole(null);
  };

  return (
    <AuthContext.Provider value={{ token, role, login, logout, getDashboardRoute }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);