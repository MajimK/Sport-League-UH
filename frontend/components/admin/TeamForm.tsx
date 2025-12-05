'use client';

import { useState } from 'react';

interface TeamFormProps {
  token: string | null;
  onSuccess: () => void;
}

export default function TeamForm({ token, onSuccess }: TeamFormProps) {
  const [formData, setFormData] = useState({
    name: '',
    description: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };

      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch('http://localhost:8000/admin/teams/', {
        method: 'POST',
        headers,
        body: JSON.stringify(formData),
        credentials: 'include'
      });

      if (!response.ok) throw new Error('Failed to create team');

      const newTeam = await response.json();
      console.log('Team created:', newTeam);

      // Limpiar formulario
      setFormData({
        name: '',
        description: ''
      });

      onSuccess();
    } catch (err) {
      setError('Error creating team');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <div className="card-body">
        <h2 className="card-title">Add Team</h2>

        {error && <div className="alert alert-danger">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group mb-3">
            <label htmlFor="name" className="form-label">Team Name</label>
            <input
              type="text"
              id="name"
              className="form-control"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
              disabled={loading}
              placeholder="Enter team name"
            />
          </div>

          <div className="form-group mb-3">
            <label htmlFor="description" className="form-label">Description</label>
            <textarea
              id="description"
              className="form-control"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              required
              disabled={loading}
              placeholder="Enter team description"
              rows={4}
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? 'Creating...' : 'Add Team'}
          </button>
        </form>
      </div>
    </div>
  );
}