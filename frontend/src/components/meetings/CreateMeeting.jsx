import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';

const CreateMeeting = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    meeting_name: '',
    meeting_date: '',
    meeting_time: '',
    location: '',
    description: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await api.post('/api/v1/meetings', formData);
      alert('Meeting created successfully!');
      navigate(`/meetings/${response.data.meeting_id}`);
    } catch (err) {
      setError('Failed to create meeting: ' + (err.response?.data?.detail || err.message));
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
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
        <h2>Create New Meeting</h2>

        {error && (
          <div style={{ 
            padding: '10px', 
            backgroundColor: '#f8d7da', 
            color: '#721c24',
            borderRadius: '4px',
            marginBottom: '20px'
          }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
              Meeting Name *
            </label>
            <input
              type="text"
              name="meeting_name"
              value={formData.meeting_name}
              onChange={handleChange}
              required
              style={{ 
                width: '100%', 
                padding: '10px', 
                border: '1px solid #ced4da',
                borderRadius: '4px',
                fontSize: '16px'
              }}
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '20px' }}>
            <div>
              <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
                Meeting Date *
              </label>
              <input
                type="date"
                name="meeting_date"
                value={formData.meeting_date}
                onChange={handleChange}
                required
                style={{ 
                  width: '100%', 
                  padding: '10px', 
                  border: '1px solid #ced4da',
                  borderRadius: '4px',
                  fontSize: '16px'
                }}
              />
            </div>

            <div>
              <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
                Meeting Time
              </label>
              <input
                type="time"
                name="meeting_time"
                value={formData.meeting_time}
                onChange={handleChange}
                style={{ 
                  width: '100%', 
                  padding: '10px', 
                  border: '1px solid #ced4da',
                  borderRadius: '4px',
                  fontSize: '16px'
                }}
              />
            </div>
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
              Location
            </label>
            <input
              type="text"
              name="location"
              value={formData.location}
              onChange={handleChange}
              placeholder="e.g., Conference Room A"
              style={{ 
                width: '100%', 
                padding: '10px', 
                border: '1px solid #ced4da',
                borderRadius: '4px',
                fontSize: '16px'
              }}
            />
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
              Description
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="5"
              placeholder="Meeting description..."
              style={{ 
                width: '100%', 
                padding: '10px', 
                border: '1px solid #ced4da',
                borderRadius: '4px',
                fontSize: '16px',
                fontFamily: 'inherit'
              }}
            />
          </div>

          <div style={{ display: 'flex', gap: '10px' }}>
            <button 
              type="submit"
              disabled={loading}
              style={{ 
                padding: '12px 24px', 
                backgroundColor: loading ? '#6c757d' : '#28a745', 
                color: 'white', 
                border: 'none',
                cursor: loading ? 'not-allowed' : 'pointer',
                borderRadius: '4px',
                fontSize: '16px',
                fontWeight: 'bold'
              }}
            >
              {loading ? 'Creating...' : 'Create Meeting'}
            </button>

            <button 
              type="button"
              onClick={() => navigate('/meetings')}
              style={{ 
                padding: '12px 24px', 
                backgroundColor: 'white', 
                color: '#6c757d', 
                border: '1px solid #6c757d',
                cursor: 'pointer',
                borderRadius: '4px',
                fontSize: '16px'
              }}
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateMeeting;
