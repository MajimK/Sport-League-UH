'use client';

import { useState, useEffect } from 'react';
import { Container, Table, Button, Modal, Form, InputGroup, Alert } from 'react-bootstrap';

interface Team {
  team_id: number;
  name: string;
  description: string;
}

interface TeamsTableProps {
  teams: Team[];
  token: string | null;
  onSuccess: () => void;
}

export default function TeamsTable({ teams, token, onSuccess }: TeamsTableProps) {
  const [deleteId, setDeleteId] = useState<number | null>(null);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');
  const [filteredTeams, setFilteredTeams] = useState<Team[]>(teams);

  useEffect(() => {
    setFilteredTeams(
      teams.filter(
        (t) =>
          t.name.toLowerCase().includes(search.toLowerCase()) ||
          t.description.toLowerCase().includes(search.toLowerCase())
      )
    );
  }, [search, teams]);

  const handleDelete = async () => {
    if (!deleteId) return;

    setDeleting(true);
    setError('');

    try {
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };

      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`http://localhost:5000/admin/teams/${deleteId}`, {
        method: 'DELETE',
        headers,
        credentials: 'include',
      });

      if (!response.ok) throw new Error('Failed to delete team');

      onSuccess();
      setDeleteId(null);
    } catch (err) {
      setError('Error deleting team');
      console.error(err);
    } finally {
      setDeleting(false);
    }
  };

  return (
    <Container className="my-4">
      <h2 className="mb-3">Teams</h2>

      {error && <Alert variant="danger">{error}</Alert>}

      {/* Search */}
      <InputGroup className="mb-3">
        <InputGroup.Text>
          <i className="bi bi-search"></i>
        </InputGroup.Text>
        <Form.Control
          placeholder="Search by name or description..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </InputGroup>

      {/* Table */}
      <div className="table-responsive">
        <Table striped hover bordered>
          <thead style={{ backgroundColor: 'var(--color-uh-red)', color: 'white' }}>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Description</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredTeams.length === 0 ? (
              <tr>
                <td colSpan={4} className="text-center">
                  No teams found
                </td>
              </tr>
            ) : (
              filteredTeams.map((team) => (
                <tr key={team.team_id}>
                  <td>{team.team_id}</td>
                  <td>{team.name}</td>
                  <td>{team.description}</td>
                  <td>
                    <Button
                      variant="danger"
                      size="sm"
                      onClick={() => setDeleteId(team.team_id)}
                      title="Delete"
                    >
                      <i className="bi bi-trash"></i>
                    </Button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </Table>
      </div>

      {/* Delete Modal */}
      <Modal show={!!deleteId} onHide={() => setDeleteId(null)} centered>
        <Modal.Header closeButton>
          <Modal.Title>Confirm Delete</Modal.Title>
        </Modal.Header>
        <Modal.Body>Are you sure you want to delete this team?</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setDeleteId(null)} disabled={deleting}>
            Cancel
          </Button>
          <Button variant="danger" onClick={handleDelete} disabled={deleting}>
            {deleting ? 'Deleting...' : 'Delete'}
          </Button>
        </Modal.Footer>
      </Modal>
    </Container>
  );
}
