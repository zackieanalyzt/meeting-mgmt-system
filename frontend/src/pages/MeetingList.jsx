import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';

const MeetingList = () => {
  const [meetings, setMeetings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState('all');
  const navigate = useNavigate();
  const { isAdmin, isGroupAdmin } = useAuth();

  useEffect(() => {
    fetchMeetings();
  }, []);

  const fetchMeetings = async () => {
    try {
      const response = await api.get('/api/v1/meetings', {
        params: { skip: 0, limit: 100 }
      });
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
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  const formatTime = (timeString) => {
    if (!timeString) return '';
    return timeString.substring(0, 5);
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8 text-center">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p className="mt-4 text-gray-600">Loading meetings...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          <p className="font-medium">Error</p>
          <p className="text-sm">{error}</p>
        </div>
        <button 
          onClick={() => navigate('/dashboard')}
          className="mt-4 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
        >
          Back to Dashboard
        </button>
      </div>
    );
  }

  const filteredMeetings = getFilteredMeetings();
  const canCreate = isAdmin() || isGroupAdmin();

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-6 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">Meetings</h1>
          <p className="text-gray-600 mt-2">Manage and view all meetings</p>
        </div>
        {canCreate && (
          <button
            onClick={() => navigate('/meetings/create')}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg transition-colors flex items-center space-x-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
            </svg>
            <span>Create Meeting</span>
          </button>
        )}
      </div>

      <div className="bg-white rounded-lg shadow-md p-4 mb-6">
        <div className="flex items-center space-x-4">
          <label className="text-sm font-medium text-gray-700">Filter by status:</label>
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="all">All ({meetings.length})</option>
            <option value="active">Active ({meetings.filter(m => m.status === 'active').length})</option>
            <option value="closed">Closed ({meetings.filter(m => m.status === 'closed').length})</option>
          </select>
        </div>
      </div>

      {filteredMeetings.length === 0 ? (
        <div className="bg-white rounded-lg shadow-md p-12 text-center">
          <svg className="mx-auto h-16 w-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <h3 className="mt-4 text-lg font-medium text-gray-900">No meetings found</h3>
          <p className="mt-2 text-gray-600">Get started by creating a new meeting</p>
          {canCreate && (
            <button
              onClick={() => navigate('/meetings/create')}
              className="mt-4 inline-block bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors"
            >
              Create First Meeting
            </button>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredMeetings.map((meeting) => (
            <div
              key={meeting.meeting_id}
              onClick={() => navigate(`/meetings/${meeting.meeting_id}`)}
              className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow cursor-pointer overflow-hidden"
            >
              <div className="p-6">
                <div className="flex justify-between items-start mb-3">
                  <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                    meeting.status === 'active' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-gray-100 text-gray-800'
                  }`}>
                    {meeting.status === 'active' ? 'Active' : 'Closed'}
                  </span>
                </div>

                <h3 className="text-lg font-bold text-gray-800 mb-2 line-clamp-2">
                  {meeting.meeting_title}
                </h3>

                <div className="space-y-2 text-sm text-gray-600">
                  <div className="flex items-center">
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <span>{formatDate(meeting.meeting_date)}</span>
                  </div>

                  <div className="flex items-center">
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span>{formatTime(meeting.start_time)} - {formatTime(meeting.end_time)}</span>
                  </div>

                  <div className="flex items-center">
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <span>{meeting.location}</span>
                  </div>

                  {meeting.created_by_fullname && (
                    <div className="flex items-center">
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                      <span className="truncate">By: {meeting.created_by_fullname}</span>
                    </div>
                  )}
                </div>

                {meeting.description && (
                  <p className="mt-3 text-sm text-gray-600 line-clamp-2">
                    {meeting.description}
                  </p>
                )}
              </div>

              <div className="bg-gray-50 px-6 py-3 border-t border-gray-200">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    navigate(`/meetings/${meeting.meeting_id}`);
                  }}
                  className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  View Details →
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MeetingList;
