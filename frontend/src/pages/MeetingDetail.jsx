import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';

const MeetingDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { isAdmin, isGroupAdmin } = useAuth();
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
      fetchMeetingDetail();
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
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  const formatTime = (timeString) => {
    if (!timeString) return 'N/A';
    return timeString.substring(0, 5);
  };

  const formatDateTime = (dateTimeString) => {
    if (!dateTimeString) return 'N/A';
    const date = new Date(dateTimeString);
    return date.toLocaleString('en-US');
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8 text-center">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p className="mt-4 text-gray-600">Loading meeting details...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
          <p className="font-medium">Error</p>
          <p className="text-sm">{error}</p>
        </div>
        <button 
          onClick={() => navigate('/meetings')}
          className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
        >
          Back to Meetings
        </button>
      </div>
    );
  }

  if (!meeting) {
    return (
      <div className="container mx-auto px-4 py-8">
        <p className="text-gray-600">Meeting not found</p>
        <button 
          onClick={() => navigate('/meetings')}
          className="mt-4 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
        >
          Back to Meetings
        </button>
      </div>
    );
  }

  const canManage = isAdmin() || isGroupAdmin();

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <div className="mb-6">
        <button 
          onClick={() => navigate('/meetings')}
          className="text-blue-600 hover:text-blue-800 mb-4"
        >
          ← Back to Meetings
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex justify-between items-start mb-6">
          <h1 className="text-3xl font-bold text-gray-800">{meeting.meeting_title}</h1>
          <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
            meeting.status === 'active' 
              ? 'bg-green-100 text-green-800' 
              : 'bg-gray-100 text-gray-800'
          }`}>
            {meeting.status === 'active' ? 'Active' : 'Closed'}
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6 p-4 bg-gray-50 rounded-lg">
          <div>
            <p className="text-sm text-gray-600 mb-1">Date</p>
            <p className="font-semibold">📅 {formatDate(meeting.meeting_date)}</p>
          </div>
          
          <div>
            <p className="text-sm text-gray-600 mb-1">Time</p>
            <p className="font-semibold">⏰ {formatTime(meeting.start_time)} - {formatTime(meeting.end_time)}</p>
          </div>
          
          <div>
            <p className="text-sm text-gray-600 mb-1">Location</p>
            <p className="font-semibold">📍 {meeting.location}</p>
          </div>
          
          {meeting.created_by_fullname && (
            <div>
              <p className="text-sm text-gray-600 mb-1">Created By</p>
              <p className="font-semibold">👤 {meeting.created_by_fullname}</p>
            </div>
          )}
        </div>

        {meeting.description && (
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">Description</h3>
            <p className="text-gray-700 leading-relaxed">{meeting.description}</p>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 p-4 bg-gray-50 rounded-lg text-sm">
          <div>
            <p className="text-gray-600 mb-1">Created</p>
            <p className="font-medium">{formatDateTime(meeting.created_at)}</p>
          </div>
          
          {meeting.updated_at && (
            <div>
              <p className="text-gray-600 mb-1">Last Updated</p>
              <p className="font-medium">{formatDateTime(meeting.updated_at)}</p>
            </div>
          )}
          
          {meeting.closed_at && (
            <div>
              <p className="text-gray-600 mb-1">Closed</p>
              <p className="font-medium">{formatDateTime(meeting.closed_at)}</p>
            </div>
          )}
        </div>

        {canManage && (
          <div className="border-t border-gray-200 pt-6 flex flex-wrap gap-3">
            <button 
              onClick={() => navigate(`/meetings/${id}/edit`)}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Edit Meeting
            </button>
            
            {meeting.status === 'active' && (
              <button 
                onClick={handleCloseMeeting}
                className="px-4 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 transition-colors"
              >
                Close Meeting
              </button>
            )}
            
            <button 
              onClick={handleDeleteMeeting}
              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              Delete Meeting
            </button>
          </div>
        )}
      </div>

      <div className="mt-6 bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-2">Agendas</h3>
        <p className="text-gray-600">Agenda management coming soon</p>
      </div>
    </div>
  );
};

export default MeetingDetail;
