// components/Logout.jsx
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function Logout() {
  const navigate = useNavigate();

  useEffect(() => {
    localStorage.removeItem('accessToken');
    navigate('/admin');
  }, [navigate]);

  return null;
}

export default Logout;
