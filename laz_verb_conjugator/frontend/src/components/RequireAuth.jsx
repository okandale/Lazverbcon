// components/RequireAuth.jsx
import { Navigate } from 'react-router-dom';

const RequireAuth = ({ children }) => {
  const token = localStorage.getItem('accessToken');
  const isAuthenticated = !!token;

  return isAuthenticated ? children : <Navigate to="/admin" />;
};

export default RequireAuth;
