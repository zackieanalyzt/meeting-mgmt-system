import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import api from '../../services/api';

const MeetingList = () => {
  const [meetings, setMeetings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState('all'); // all, active, closed
  const navigate = useNavigate();
  const { isAdmin } = useAuth();

  useEffect(() => {
    fetchMeetings();
  }, []);

  const fetchMeetings = async () => {
    try {
      const response = await api.get('/api/v1/meetings');
      setMeetings(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch meetings: ' + (err.response?.data?.detail || err.message));
      setLoading(false);
    }
  };

  const getFilteredMeetings = () => {
    if (filter === 'all') return meetings;
    return meetings.filter(m => m.status === filter);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('th-TH', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  if (loading) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <p>Loading meetings...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '20px' }}>
        <div style={{ color: 'red', marginBottom: '20px' }}>{error}</div>
        <button onClick={() => navigate('/dashboard')}>Back to Dashboard</button>
      </div>
    );
  }

  const filteredMeetings = getFilteredMeetings();

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2>Meetings</h2>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button 
            onClick={() => navigate('/dashboard')}
            style={{ 
              padding: '8px 16px', 
              backgroundColor: '#6c757d', 
              color: 'white', 
              border: 'none',
              cursor: 'pointer',
              borderRadius: '4px'
            }}
          >
            Back to Dashboard
          </button>
          {isAdmin() && (
            <button 
              onClick={() => navigate('/meetings/create')}
              style={{ 
                padding: '8px 16px', 
                backgroundColor: '#28a745', 
                color: 'white', 
                border: 'none',
                cursor: 'pointer',
                borderRadius: '4px'
              }}
            >
              Create Meeting
            </button>
          )}
        </div>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <label style={{ marginRight: '10px' }}>Filter:</label>
        <select 
          value={filter} 
          onChange={(e) => setFilter(e.target.value)}
          style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
        >
          <option value="all">All Meetings ({meetings.length})</option>
          <option value="active">Active ({meetings.filter(m => m.status === 'active').length})</option>
          <option value="closed">Closed ({meetings.filter(m => m.status === 'closed').length})</option>
        </select>
      </div>

      {filteredMeetings.length === 0 ? (
        <div style={{ 
          textAlign: 'center', 
          padding: '40px', 
          backgroundColor: '#f8f9fa',
          borderRadius: '8px'
        }}>
          <p>No meetings found.</p>
          {isAdmin() && (
            <button 
              onClick={() => navigate('/meetings/create')}
              style={{ 
                marginTop: '10px',
                padding: '10px 20px', 
                backgroundColor: '#28a745', 
                color: 'white', 
                border: 'none',
                cursor: 'pointer',
                borderRadius: '4px'
              }}
            >
              Create First Meeting
            </button>
          )}
        </div>
      ) : (
        <div style={{ display: 'grid', gap: '15px' }}>
          {filteredMeetings.map((meeting) => (
            <div 
              key={meeting.meeting_id}
              onClick={() => navigate(`/meetings/${meeting.meeting_id}`)}
              style={{ 
                padding: '20px',
                backgroundColor: 'white',
                border: '1px solid #dee2e6',
                borderRadius: '8px',
                cursor: 'pointer',
                transition: 'box-shadow 0.2s',
                boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
              }}
              onMouseEnter={(e) => e.currentTarget.style.boxShadow = '0 4px 8px rgba(0,0,0,0.15)'}
              onMouseLeave={(e) => e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)'}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                <div style={{ flex: 1 }}>
                  <h3 style={{ margin: '0 0 10px 0' }}>{meeting.meeting_name}</h3>
                  <p style={{ margin: '5px 0', color: '#6c757d' }}>
                    📅 {formatDate(meeting.meeting_date)}
                    {meeting.meeting_time && ` • ⏰ ${meeting.meeting_time}`}
                  </p>
                  {meeting.location && (
                    <p style={{ margin: '5px 0', color: '#6c757d' }}>
                      📍 {meeting.location}
                    </p>
                  )}
                  {meeting.description && (
                    <p style={{ margin: '10px 0 0 0', color: '#495057' }}>
                      {meeting.description.length > 150 
                        ? meeting.description.substring(0, 150) + '...' 
                        : meeting.description}
                    </p>
                  )}
                </div>
                <div>
                  <span style={{ 
                    padding: '4px 12px',
                    borderRadius: '12px',
                    fontSize: '12px',
                    fontWeight: 'bold',
                    backgroundColor: meeting.status === 'active' ? '#d4edda' : '#e2e3e5',
                    color: meeting.status === 'active' ? '#155724' : '#383d41'
                  }}>
                    {meeting.status === 'active' ? 'Active' : 'Closed'}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MeetingList;
