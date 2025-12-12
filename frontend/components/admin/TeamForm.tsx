'use client';

import { useState, useEffect } from 'react';

interface TeamFormProps {
  onSuccess: () => void;
}

interface Game {
  game_id: number;
  name: string;
}

export default function TeamForm({ onSuccess }: TeamFormProps) {
  const API_URL = process.env.NEXT_PUBLIC_API_URL;

  const [formData, setFormData] = useState({
    name: '',
    description: '',
    game_id: ''
  });
  const [games, setGames] = useState<Game[]>([]);
  const [loading, setLoading] = useState(false);
  const [fetchingGames, setFetchingGames] = useState(true);
  const [error, setError] = useState('');

  // Fetch games on component mount - SIN TOKEN
  useEffect(() => {
    const fetchGames = async () => {
      console.log('🔵 TeamForm: Fetching games without token...');

      try {
        const response = await fetch(`${API_URL}/admin/games/`, {
          headers: {
            'Content-Type': 'application/json',
          },
          credentials: 'include'
        });

        console.log('🟡 TeamForm: Response status:', response.status);

        if (!response.ok) {
          const errorText = await response.text();
          console.error('❌ TeamForm: Error response:', errorText);
          throw new Error(`Failed to fetch games: ${response.status}`);
        }

        const gamesData = await response.json();
        console.log('✅ TeamForm: Games data received:', gamesData);

        if (!Array.isArray(gamesData)) {
          console.error('❌ TeamForm: gamesData is not an array:', gamesData);
          throw new Error('Invalid response format: expected array');
        }

        setGames(gamesData);
        setError('');

      } catch (err) {
        console.error('❌ TeamForm: Error in fetchGames:', err);
        setError(err instanceof Error ? err.message : 'Failed to load sports');
        setGames([]);
      } finally {
        console.log('✅ TeamForm: Setting fetchingGames to false');
        setFetchingGames(false);
      }
    };

    fetchGames();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log('🔵 TeamForm: Submitting form');
    setLoading(true);
    setError('');

    try {
      // Validation
      if (!formData.name.trim()) {
        throw new Error('Team name is required');
      }

      if (!formData.game_id) {
        throw new Error('Please select a sport');
      }

      // Prepare data with game_id as number
      const requestData = {
        name: formData.name.trim(),
        description: formData.description.trim(),
        game_id: parseInt(formData.game_id, 10)
      };

      console.log('🟡 TeamForm: Submitting team data:', requestData);

      const response = await fetch(`${API_URL}/admin/teams/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
        credentials: 'include'
      });

      console.log('🟡 TeamForm: Create team response status:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('❌ TeamForm: Error response text:', errorText);
        throw new Error(`Failed to create team: ${response.status}`);
      }

      const newTeam = await response.json();
      console.log('✅ TeamForm: Team created:', newTeam);

      // Reset form
      setFormData({
        name: '',
        description: '',
        game_id: ''
      });

      onSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error creating team');
      console.error('❌ TeamForm: Submit error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  console.log('🎨 TeamForm rendering state:', {
    fetchingGames,
    gamesCount: games.length,
    loading,
    error
  });

  if (fetchingGames) {
    console.log('🔄 TeamForm: Showing loading state');
    return (
      <div className="card">
        <div className="card-body text-center">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading sports...</span>
          </div>
          <p className="mt-2">Loading available sports...</p>
        </div>
      </div>
    );
  }

  console.log('🎨 TeamForm: Rendering form with', games.length, 'games');

  return (
    <div className="card shadow-sm">
      <div className="card-body">
        <h2 className="card-title h4 mb-4">Create New Team</h2>

        {error && (
          <div className="alert alert-danger alert-dismissible fade show" role="alert">
            <strong>Error:</strong> {error}
            <button
              type="button"
              className="btn-close"
              onClick={() => setError('')}
              aria-label="Close"
            ></button>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="name" className="form-label fw-semibold">
              Team Name <span className="text-danger">*</span>
            </label>
            <input
              type="text"
              id="name"
              name="name"
              className="form-control"
              value={formData.name}
              onChange={handleChange}
              required
              disabled={loading}
              placeholder="Enter team name"
              minLength={2}
              maxLength={100}
            />
          </div>

          <div className="mb-3">
            <label htmlFor="game_id" className="form-label fw-semibold">
              Sport <span className="text-danger">*</span>
            </label>
            <select
              id="game_id"
              name="game_id"
              className="form-select"
              value={formData.game_id}
              onChange={handleChange}
              required
              disabled={loading || games.length === 0}
            >
              <option value="">Select a sport</option>
              {games.map((game) => (
                <option key={game.game_id} value={game.game_id}>
                  {game.name}
                </option>
              ))}
            </select>
            {games.length === 0 ? (
              <div className="alert alert-warning mt-2 py-2">
                <i className="bi bi-exclamation-triangle me-2"></i>
                No sports available. Please create sports first.
              </div>
            ) : (
              <div className="form-text">
                {games.length} sport{games.length !== 1 ? 's' : ''} available
              </div>
            )}
          </div>

          <div className="mb-4">
            <label htmlFor="description" className="form-label fw-semibold">
              Description
            </label>
            <textarea
              id="description"
              name="description"
              className="form-control"
              value={formData.description}
              onChange={handleChange}
              disabled={loading}
              placeholder="Optional: Enter team description"
              rows={3}
              maxLength={500}
            />
            <div className="form-text">
              Optional field. Maximum 500 characters.
            </div>
          </div>

          <button
            type="submit"
            className="btn btn-primary px-4"
            disabled={loading || !formData.name.trim() || !formData.game_id || games.length === 0}
          >
            {loading ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                Creating Team...
              </>
            ) : (
              'Create Team'
            )}
          </button>
        </form>

        <div className="mt-4 pt-3 border-top">
          <small className="text-muted">
            {games.length > 0 ? (
              `Ready to create teams for ${games.length} sports`
            ) : (
              'No sports available. Add sports first.'
            )}
          </small>
        </div>
      </div>
    </div>
  );
}