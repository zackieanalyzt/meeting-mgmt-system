import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../../services/api';

const MeetingDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
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
      setError('Failed to fetch meeting details');
      setLoading(false);
    }
  };

  if (loading) return <div>Loading meeting details...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;
  if (!meeting) return <div>Meeting not found</div>;

  return (
    <div style={{ padding: '20px' }}>
      <button onClick={() => navigate('/meetings')} style={{ marginBottom: '20px' }}>
        ← Back to Meetings
      </button>
      
      <h2>{meeting.title}</h2>
      <p><strong>Date:</strong> {meeting.date}</p>
      <p><strong>Location:</strong> {meeting.location}</p>
      <p><strong>Description:</strong> {meeting.description}</p>
      
      {meeting.agendas && meeting.agendas.length > 0 && (
        <div style={{ marginTop: '20px' }}>
          <h3>Agendas:</h3>
          <ul>
            {meeting.agendas.map((agenda) => (
              <li key={agenda.id}>{agenda.title}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default MeetingDetail;
