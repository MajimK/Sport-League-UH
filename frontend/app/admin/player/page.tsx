'use client';

import { useState, useEffect } from 'react';
import PlayerForm from '@components/admin/PlayerForm';
import PlayersTable from '@components/admin/PlayersTable';

interface Player {
  player_id: number;
  name: string;
  CI: string;
  faculty: string;
}

export default function ManagePlayersPage() {
  const API_URL = process.env.NEXT_PUBLIC_API_URL;

  const [players, setPlayers] = useState<Player[]>([]);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    // Obtener token del localStorage
    const storedToken = localStorage.getItem('access_token');
    setToken(storedToken);
    fetchPlayers(storedToken);
  }, []);

  const fetchPlayers = async (authToken: string | null) => {
    try {
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };

      if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`;
      }

      const response = await fetch(`${API_URL}/admin/players/`, {
        headers,
        credentials: 'include'
      });

      if (!response.ok) throw new Error('Failed to fetch players');

      const playersData = await response.json();
      setPlayers(playersData);
    } catch (err) {
      console.error('Error loading players:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = () => {
    fetchPlayers(token);
  };

  if (loading) return <div className="container mt-4">Loading...</div>;

  return (
    <div className="container mt-4">
      <h1 className="mb-4">Manage Players</h1>
      <div className="row">
        <div className="col-md-6">
          <PlayerForm
            token={token}
            onSuccess={handleRefresh}
          />
        </div>
        <div className="col-md-6">
          <PlayersTable
            players={players}
            token={token}
            onSuccess={handleRefresh}
          />
        </div>
      </div>
    </div>
  );
}