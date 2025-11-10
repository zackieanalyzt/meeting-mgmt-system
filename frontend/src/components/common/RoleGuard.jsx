import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const RoleGuard = ({ children, allowedRoles, fallback = '/dashboard' }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!user) {
    return <Navigate to="/login" />;
  }

  // Check if user has any of the allowed roles
  const hasPermission = allowedRoles.some(role => 
    user.roles?.includes(role)
  );

  if (!hasPermission) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <h2>Access Denied</h2>
        <p>You don't have permission to access this page.</p>
        <p>Required roles: {allowedRoles.join(', ')}</p>
        <button onClick={() => window.location.href = fallback}>
          Go to Dashboard
        </button>
      </div>
    );
  }

  return children;
};

export default RoleGuard;
