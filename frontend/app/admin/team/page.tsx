'use client';

import { useState, useEffect } from 'react';
import TeamForm from '@components/admin/TeamForm';
import TeamsTable from '@components/admin/TeamsTable';
import { Container, Row, Col, Spinner } from 'react-bootstrap';

interface Team {
  team_id: number;
  name: string;
  description: string;
}

export default function ManageTeamsPage() {
  const API_URL = process.env.NEXT_PUBLIC_API_URL;
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

      const response = await fetch(`${API_URL}/admin/teams/`, {
        headers,
        credentials: 'include',
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

  const handleRefresh = () => fetchTeams(token);

  if (loading) {
    return (
      <Container className="mt-4 text-center">
        <Spinner animation="border" variant="danger" />
        <p className="mt-2">Loading Teams...</p>
      </Container>
    );
  }

  return (
    <Container className="mt-4">

      <h1 className="mb-4" style={{ color: 'var(--color-uh-red)' }}>
        Manage Teams
      </h1>

      <Row className="g-4">

        {/* Form for creating/editing teams */}
        <Col md={6}>
          <TeamForm onSuccess={handleRefresh} />
        </Col>
        {/* Table of existing teams */}
        <Col md={6}>
          <TeamsTable teams={teams} token={token} onSuccess={handleRefresh} />
        </Col>

      </Row>
    </Container>
  );
}
