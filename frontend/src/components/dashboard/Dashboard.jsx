import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const Dashboard = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, navigate]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (!isAuthenticated || !user) {
    return <div>Loading...</div>;
  }

  return (
    <div style={{ padding: '20px' }}>
      <h1>Dashboard</h1>
      <p>Welcome, {user.username || user.email || 'User'}!</p>
      
      <div style={{ marginTop: '20px' }}>
        <h3>User Information:</h3>
        <ul>
          <li>Username: {user.username}</li>
          <li>Email: {user.email}</li>
          {user.role && <li>Role: {user.role}</li>}
        </ul>
      </div>

      <button 
        onClick={handleLogout}
        style={{ 
          marginTop: '20px',
          padding: '10px 20px', 
          backgroundColor: '#dc3545', 
          color: 'white', 
          border: 'none',
          cursor: 'pointer'
        }}
      >
        Logout
      </button>
    </div>
  );
};

export default Dashboard;
