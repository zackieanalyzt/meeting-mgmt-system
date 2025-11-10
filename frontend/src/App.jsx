import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import LoginForm from './components/auth/LoginForm';
import Dashboard from './components/dashboard/Dashboard';
import MeetingList from './components/meetings/MeetingList';
import MeetingDetail from './components/meetings/MeetingDetail';
import CreateMeeting from './components/meetings/CreateMeeting';
import RoleGuard from './components/common/RoleGuard';

// Protected Route wrapper
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return <div>Loading...</div>;
  }
  
  return isAuthenticated ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<LoginForm />} />
          
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          
          <Route 
            path="/meetings" 
            element={
              <ProtectedRoute>
                <MeetingList />
              </ProtectedRoute>
            } 
          />
          
          <Route 
            path="/meetings/create" 
            element={
              <ProtectedRoute>
                <RoleGuard allowedRoles={['Admin ใหญ่']}>
                  <CreateMeeting />
                </RoleGuard>
              </ProtectedRoute>
            } 
          />
          
          <Route 
            path="/meetings/:id" 
            element={
              <ProtectedRoute>
                <MeetingDetail />
              </ProtectedRoute>
            } 
          />
          
          <Route path="/" element={<Navigate to="/dashboard" />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
