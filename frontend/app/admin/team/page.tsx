'use client';

import { useState, useEffect } from 'react';
import TeamForm from '@components/admin/TeamForm';
import TeamsTable from '@components/admin/TeamsTable';

interface Team {
  team_id: number;
  name: string;
  description: string;
}

export default function ManageTeamsPage() {
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const storedToken = localStorage.getItem('access_token');
    setToken(storedToken);
    fetchTeams(storedToken);
  }, []);

  const fetchTeams = async (authToken: string | null) => {
    try {
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };
      
      if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`;
      }

      const response = await fetch('http://localhost:5000/admin/teams/', {
        headers,
        credentials: 'include'
      });

      if (!response.ok) throw new Error('Failed to fetch teams');

      const teamsData = await response.json();
      setTeams(teamsData);
    } catch (err) {
      console.error('Error loading teams:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = () => {
    fetchTeams(token);
  };

  if (loading) return <div className="container mt-4">Loading...</div>;

  return (
    <div className="container mt-4">
      <h1 className="mb-4">Manage Teams</h1>
      <div className="row">
        <div className="col-md-6">
          <TeamForm 
            token={token}
            onSuccess={handleRefresh}
          />
        </div>
        <div className="col-md-6">
          <TeamsTable 
            teams={teams}
            token={token}
            onSuccess={handleRefresh}
          />
        </div>
      </div>
    </div>
  );
}