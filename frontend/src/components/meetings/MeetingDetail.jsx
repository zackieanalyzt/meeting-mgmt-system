import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import api from '../../services/api';

const MeetingDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { isAdmin } = useAuth();
  const [meeting, setMeeting] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchMeetingDetail();
  }, [id]);

  const fetchMeetingDetail = async () => {
    try {
      const response = await api.get(`/api/v1/meetings/${id}`);
      setMeeting(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch meeting details: ' + (err.response?.data?.detail || err.message));
      setLoading(false);
    }
  };

  const handleCloseMeeting = async () => {
    if (!window.confirm('Are you sure you want to close this meeting?')) {
      return;
    }

    try {
      await api.post(`/api/v1/meetings/${id}/close`);
      alert('Meeting closed successfully');
      fetchMeetingDetail(); // Refresh data
    } catch (err) {
      alert('Failed to close meeting: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleDeleteMeeting = async () => {
    if (!window.confirm('Are you sure you want to delete this meeting? This action cannot be undone.')) {
      return;
    }

    try {
      await api.delete(`/api/v1/meetings/${id}`);
      alert('Meeting deleted successfully');
      navigate('/meetings');
    } catch (err) {
      alert('Failed to delete meeting: ' + (err.response?.data?.detail || err.message));
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('th-TH', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  const formatDateTime = (dateTimeString) => {
    if (!dateTimeString) return 'N/A';
    const date = new Date(dateTimeString);
    return date.toLocaleString('th-TH');
  };

  if (loading) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <p>Loading meeting details...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '20px' }}>
        <div style={{ color: 'red', marginBottom: '20px' }}>{error}</div>
        <button onClick={() => navigate('/meetings')}>Back to Meetings</button>
      </div>
    );
  }

  if (!meeting) {
    return (
      <div style={{ padding: '20px' }}>
        <p>Meeting not found</p>
        <button onClick={() => navigate('/meetings')}>Back to Meetings</button>
      </div>
    );
  }

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ marginBottom: '20px' }}>
        <button 
          onClick={() => navigate('/meetings')}
          style={{ 
            padding: '8px 16px', 
            backgroundColor: '#6c757d', 
            color: 'white', 
            border: 'none',
            cursor: 'pointer',
            borderRadius: '4px'
          }}
        >
          ← Back to Meetings
        </button>
      </div>

      <div style={{ 
        backgroundColor: 'white',
        border: '1px solid #dee2e6',
        borderRadius: '8px',
        padding: '30px'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '20px' }}>
          <h1 style={{ margin: 0 }}>{meeting.meeting_name}</h1>
          <span style={{ 
            padding: '6px 16px',
            borderRadius: '12px',
            fontSize: '14px',
            fontWeight: 'bold',
            backgroundColor: meeting.status === 'active' ? '#d4edda' : '#e2e3e5',
            color: meeting.status === 'active' ? '#155724' : '#383d41'
          }}>
            {meeting.status === 'active' ? 'Active' : 'Closed'}
          </span>
        </div>

        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
          gap: '20px',
          marginBottom: '30px',
          padding: '20px',
          backgroundColor: '#f8f9fa',
          borderRadius: '8px'
        }}>
          <div>
            <p style={{ margin: '0 0 5px 0', color: '#6c757d', fontSize: '14px' }}>Date</p>
            <p style={{ margin: 0, fontWeight: 'bold' }}>📅 {formatDate(meeting.meeting_date)}</p>
          </div>
          
          {meeting.meeting_time && (
            <div>
              <p style={{ margin: '0 0 5px 0', color: '#6c757d', fontSize: '14px' }}>Time</p>
              <p style={{ margin: 0, fontWeight: 'bold' }}>⏰ {meeting.meeting_time}</p>
            </div>
          )}
          
          {meeting.location && (
            <div>
              <p style={{ margin: '0 0 5px 0', color: '#6c757d', fontSize: '14px' }}>Location</p>
              <p style={{ margin: 0, fontWeight: 'bold' }}>📍 {meeting.location}</p>
            </div>
          )}
        </div>

        {meeting.description && (
          <div style={{ marginBottom: '30px' }}>
            <h3>Description</h3>
            <p style={{ lineHeight: '1.6', color: '#495057' }}>{meeting.description}</p>
          </div>
        )}

        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '15px',
          marginBottom: '30px',
          padding: '15px',
          backgroundColor: '#f8f9fa',
          borderRadius: '8px',
          fontSize: '14px'
        }}>
          <div>
            <p style={{ margin: '0 0 5px 0', color: '#6c757d' }}>Created</p>
            <p style={{ margin: 0 }}>{formatDateTime(meeting.created_at)}</p>
          </div>
          
          {meeting.updated_at && (
            <div>
              <p style={{ margin: '0 0 5px 0', color: '#6c757d' }}>Last Updated</p>
              <p style={{ margin: 0 }}>{formatDateTime(meeting.updated_at)}</p>
            </div>
          )}
          
          {meeting.closed_at && (
            <div>
              <p style={{ margin: '0 0 5px 0', color: '#6c757d' }}>Closed</p>
              <p style={{ margin: 0 }}>{formatDateTime(meeting.closed_at)}</p>
            </div>
          )}
        </div>

        {isAdmin() && (
          <div style={{ 
            borderTop: '1px solid #dee2e6',
            paddingTop: '20px',
            display: 'flex',
            gap: '10px',
            flexWrap: 'wrap'
          }}>
            <button 
              onClick={() => navigate(`/meetings/${id}/edit`)}
              style={{ 
                padding: '10px 20px', 
                backgroundColor: '#007bff', 
                color: 'white', 
                border: 'none',
                cursor: 'pointer',
                borderRadius: '4px'
              }}
            >
              Edit Meeting
            </button>
            
            {meeting.status === 'active' && (
              <button 
                onClick={handleCloseMeeting}
                style={{ 
                  padding: '10px 20px', 
                  backgroundColor: '#ffc107', 
                  color: '#000', 
                  border: 'none',
                  cursor: 'pointer',
                  borderRadius: '4px'
                }}
              >
                Close Meeting
              </button>
            )}
            
            <button 
              onClick={handleDeleteMeeting}
              style={{ 
                padding: '10px 20px', 
                backgroundColor: '#dc3545', 
                color: 'white', 
                border: 'none',
                cursor: 'pointer',
                borderRadius: '4px'
              }}
            >
              Delete Meeting
            </button>
          </div>
        )}
      </div>

      <div style={{ 
        marginTop: '30px',
        backgroundColor: 'white',
        border: '1px solid #dee2e6',
        borderRadius: '8px',
        padding: '30px'
      }}>
        <h3>Agendas</h3>
        <p style={{ color: '#6c757d' }}>Agenda management coming in Phase 9.3</p>
      </div>
    </div>
  );
};

export default MeetingDetail;
