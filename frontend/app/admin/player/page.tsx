'use client';

import { useState, useEffect } from 'react';
import PlayerForm from '@components/admin/PlayerForm';
import PlayersTable from '@components/admin/PlayersTable';
import { Container, Row, Col, Spinner } from 'react-bootstrap';

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
        credentials: 'include',
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

  const handleRefresh = () => fetchPlayers(token);

  if (loading) {
    return (
      <Container className="mt-4 text-center">
        <Spinner animation="border" variant="danger" />
        <p className="mt-2">Loading Players...</p>
      </Container>
    );
  }

  return (
    <Container className="mt-4">

      <h1 className="mb-4" style={{ color: 'var(--color-uh-red)' }}>
        Manage Players
      </h1>

      <Row className="g-4">

        {/* Form for creating/editing players */}
        <Col md={6}>
          <PlayerForm token={token} onSuccess={handleRefresh} />
        </Col>

        {/* Table of existing players */}
        <Col md={6}>
          <PlayersTable players={players} token={token} onSuccess={handleRefresh} />
        </Col>

      </Row>
    </Container>
  );
}
