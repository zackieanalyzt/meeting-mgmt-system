import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import api from '../../services/api';

const Dashboard = () => {
  const { user, isAuthenticated, logout, isAdmin, isGroupAdmin } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    totalMeetings: 0,
    activeMeetings: 0,
    closedMeetings: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    } else {
      fetchStats();
    }
  }, [isAuthenticated, navigate]);

  const fetchStats = async () => {
    try {
      const response = await api.get('/api/v1/meetings');
      const meetings = response.data;
      
      setStats({
        totalMeetings: meetings.length,
        activeMeetings: meetings.filter(m => m.status === 'active').length,
        closedMeetings: meetings.filter(m => m.status === 'closed').length
      });
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (!isAuthenticated || !user) {
    return <div>Loading...</div>;
  }

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
        <h1>Dashboard</h1>
        <button 
          onClick={handleLogout}
          style={{ 
            padding: '10px 20px', 
            backgroundColor: '#dc3545', 
            color: 'white', 
            border: 'none',
            cursor: 'pointer',
            borderRadius: '4px'
          }}
        >
          Logout
        </button>
      </div>

      <div style={{ 
        backgroundColor: '#f8f9fa', 
        padding: '20px', 
        borderRadius: '8px',
        marginBottom: '30px'
      }}>
        <h2>Welcome, {user.fullname || user.username}!</h2>
        <div style={{ marginTop: '15px' }}>
          <p><strong>Username:</strong> {user.username}</p>
          <p><strong>Email:</strong> {user.email}</p>
          <p><strong>Department:</strong> {user.department}</p>
          <p><strong>Roles:</strong> {user.roles?.join(', ') || 'No roles assigned'}</p>
        </div>
      </div>

      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
        gap: '20px',
        marginBottom: '30px'
      }}>
        <div style={{ 
          backgroundColor: '#007bff', 
          color: 'white', 
          padding: '20px', 
          borderRadius: '8px',
          textAlign: 'center'
        }}>
          <h3 style={{ margin: '0 0 10px 0' }}>{loading ? '...' : stats.totalMeetings}</h3>
          <p style={{ margin: 0 }}>Total Meetings</p>
        </div>
        
        <div style={{ 
          backgroundColor: '#28a745', 
          color: 'white', 
          padding: '20px', 
          borderRadius: '8px',
          textAlign: 'center'
        }}>
          <h3 style={{ margin: '0 0 10px 0' }}>{loading ? '...' : stats.activeMeetings}</h3>
          <p style={{ margin: 0 }}>Active Meetings</p>
        </div>
        
        <div style={{ 
          backgroundColor: '#6c757d', 
          color: 'white', 
          padding: '20px', 
          borderRadius: '8px',
          textAlign: 'center'
        }}>
          <h3 style={{ margin: '0 0 10px 0' }}>{loading ? '...' : stats.closedMeetings}</h3>
          <p style={{ margin: 0 }}>Closed Meetings</p>
        </div>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h3>Quick Actions</h3>
        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          <button 
            onClick={() => navigate('/meetings')}
            style={{ 
              padding: '10px 20px', 
              backgroundColor: '#007bff', 
              color: 'white', 
              border: 'none',
              cursor: 'pointer',
              borderRadius: '4px'
            }}
          >
            View All Meetings
          </button>
          
          {isAdmin() && (
            <button 
              onClick={() => navigate('/meetings/create')}
              style={{ 
                padding: '10px 20px', 
                backgroundColor: '#28a745', 
                color: 'white', 
                border: 'none',
                cursor: 'pointer',
                borderRadius: '4px'
              }}
            >
              Create New Meeting
            </button>
          )}
          
          {isGroupAdmin() && (
            <button 
              onClick={() => navigate('/agendas')}
              style={{ 
                padding: '10px 20px', 
                backgroundColor: '#17a2b8', 
                color: 'white', 
                border: 'none',
                cursor: 'pointer',
                borderRadius: '4px'
              }}
            >
              Manage Agendas
            </button>
          )}
        </div>
      </div>

      <div style={{ 
        backgroundColor: '#fff3cd', 
        padding: '15px', 
        borderRadius: '8px',
        border: '1px solid #ffc107'
      }}>
        <h4 style={{ margin: '0 0 10px 0' }}>Your Permissions:</h4>
        <ul style={{ margin: 0, paddingLeft: '20px' }}>
          {isAdmin() && (
            <>
              <li>Create and manage meetings</li>
              <li>Approve agendas</li>
              <li>Close meetings</li>
              <li>Manage reports</li>
            </>
          )}
          {isGroupAdmin() && !isAdmin() && (
            <>
              <li>Add agendas to meetings</li>
              <li>Upload files</li>
              <li>Edit content before meeting closure</li>
            </>
          )}
          {!isAdmin() && !isGroupAdmin() && (
            <>
              <li>View meetings and agendas</li>
              <li>Search reports</li>
            </>
          )}
        </ul>
      </div>
    </div>
  );
};

export default Dashboard;
