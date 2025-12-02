'use client';

import { useState } from 'react';

interface PlayerFormProps {
  token: string | null;
  onSuccess: () => void;
}

export default function PlayerForm({ token, onSuccess }: PlayerFormProps) {
  const [formData, setFormData] = useState({
    CI: '',
    name: '',
    faculty: ''
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

      const response = await fetch('http://localhost:5000/admin/players/', {
        method: 'POST',
        headers,
        body: JSON.stringify(formData),
        credentials: 'include'
      });

      if (!response.ok) throw new Error('Failed to create player');

      const newPlayer = await response.json();
      console.log('Player created:', newPlayer);

      // Limpiar formulario
      setFormData({
        CI: '',
        name: '',
        faculty: ''
      });
      
      onSuccess();
    } catch (err) {
      setError('Error creating player');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <div className="card-body">
        <h2 className="card-title">Add Player</h2>
        
        {error && <div className="alert alert-danger">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group mb-3">
            <label htmlFor="CI" className="form-label">CI (Identification)</label>
            <input
              type="text"
              id="CI"
              className="form-control"
              value={formData.CI}
              onChange={(e) => setFormData({...formData, CI: e.target.value})}
              required
              disabled={loading}
              placeholder="Enter CI number"
            />
          </div>

          <div className="form-group mb-3">
            <label htmlFor="name" className="form-label">Name</label>
            <input
              type="text"
              id="name"
              className="form-control"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              required
              disabled={loading}
              placeholder="Enter full name"
            />
          </div>

          <div className="form-group mb-3">
            <label htmlFor="faculty" className="form-label">Faculty</label>
            <input
              type="text"
              id="faculty"
              className="form-control"
              value={formData.faculty}
              onChange={(e) => setFormData({...formData, faculty: e.target.value})}
              required
              disabled={loading}
              placeholder="Enter faculty name"
            />
          </div>

          <button 
            type="submit" 
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? 'Creating...' : 'Add Player'}
          </button>
        </form>
      </div>
    </div>
  );
}