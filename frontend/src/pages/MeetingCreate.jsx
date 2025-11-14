import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const MeetingCreate = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    meeting_title: '',
    meeting_date: '',
    start_time: '',
    end_time: '',
    location: '',
    description: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const validateForm = () => {
    if (formData.start_time && formData.end_time) {
      if (formData.end_time <= formData.start_time) {
        setError('End time must be after start time');
        return false;
      }
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    
    if (!validateForm()) {
      return;
    }
    
    setLoading(true);

    try {
      const response = await api.post('/api/v1/meetings', formData);
      setSuccess('Meeting created successfully! Redirecting...');
      setTimeout(() => {
        navigate(`/meetings/${response.data.meeting_id}`);
      }, 1500);
    } catch (err) {
      setError('Failed to create meeting: ' + (err.response?.data?.detail || err.message));
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="mb-6">
          <button 
            onClick={() => navigate('/meetings')}
            className="text-blue-600 hover:text-blue-800 mb-4"
          >
            ← Back to Meetings
          </button>
          <h1 className="text-3xl font-bold text-gray-800">Create New Meeting</h1>
          <p className="text-gray-600 mt-2">Fill in the meeting details</p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
            <p className="font-medium">Error</p>
            <p className="text-sm">{error}</p>
          </div>
        )}

        {success && (
          <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg mb-4">
            <p className="font-medium">Success!</p>
            <p className="text-sm">{success}</p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="meeting_title" className="block text-sm font-medium text-gray-700 mb-2">
              Meeting Title <span className="text-red-500">*</span>
            </label>
            <input
              id="meeting_title"
              name="meeting_title"
              type="text"
              value={formData.meeting_title}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="e.g., Board Meeting Q4 2024"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label htmlFor="meeting_date" className="block text-sm font-medium text-gray-700 mb-2">
                Meeting Date <span className="text-red-500">*</span>
              </label>
              <input
                id="meeting_date"
                name="meeting_date"
                type="date"
                value={formData.meeting_date}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label htmlFor="start_time" className="block text-sm font-medium text-gray-700 mb-2">
                Start Time <span className="text-red-500">*</span>
              </label>
              <input
                id="start_time"
                name="start_time"
                type="time"
                value={formData.start_time}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label htmlFor="end_time" className="block text-sm font-medium text-gray-700 mb-2">
                End Time <span className="text-red-500">*</span>
              </label>
              <input
                id="end_time"
                name="end_time"
                type="time"
                value={formData.end_time}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          <div>
            <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-2">
              Location <span className="text-red-500">*</span>
            </label>
            <input
              id="location"
              name="location"
              type="text"
              value={formData.location}
              onChange={handleChange}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="e.g., Conference Room A"
            />
          </div>

          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="4"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Meeting description..."
            />
          </div>

          <div className="flex justify-end space-x-4 pt-4">
            <button
              type="button"
              onClick={() => navigate('/meetings')}
              className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
              disabled={loading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
              disabled={loading}
            >
              {loading ? 'Creating...' : 'Create Meeting'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default MeetingCreate;
