import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';

const MeetingList = () => {
  const [meetings, setMeetings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchMeetings();
  }, []);

  const fetchMeetings = async () => {
    try {
      const response = await api.get('/api/v1/meetings');
      setMeetings(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch meetings');
      setLoading(false);
    }
  };

  if (loading) return <div>Loading meetings...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div style={{ padding: '20px' }}>
      <h2>Meetings</h2>
      {meetings.length === 0 ? (
        <p>No meetings found.</p>
      ) : (
        <ul>
          {meetings.map((meeting) => (
            <li 
              key={meeting.id}
              onClick={() => navigate(`/meetings/${meeting.id}`)}
              style={{ cursor: 'pointer', marginBottom: '10px' }}
            >
              {meeting.title} - {meeting.date}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MeetingList;
