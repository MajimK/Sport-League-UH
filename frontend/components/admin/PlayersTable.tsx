'use client';

import { useState, useEffect } from 'react';
import { Container, Table, Button, Modal, Form, InputGroup, Alert } from 'react-bootstrap';

interface Player {
  player_id: number;
  name: string;
  CI: string;
  faculty: string;
}

interface PlayersTableProps {
  players: Player[];
  token: string | null;
  onSuccess: () => void;
}

export default function PlayersTable({ players, token, onSuccess }: PlayersTableProps) {
  const [deleteId, setDeleteId] = useState<number | null>(null);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');
  const [filteredPlayers, setFilteredPlayers] = useState<Player[]>(players);

  useEffect(() => {
    setFilteredPlayers(
      players.filter(
        (p) =>
          p.name.toLowerCase().includes(search.toLowerCase()) ||
          p.faculty.toLowerCase().includes(search.toLowerCase()) ||
          p.CI.includes(search)
      )
    );
  }, [search, players]);

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

      const response = await fetch(`http://localhost:5000/admin/players/${deleteId}`, {
        method: 'DELETE',
        headers,
        credentials: 'include',
      });

      if (!response.ok) throw new Error('Failed to delete player');

      onSuccess();
      setDeleteId(null);
    } catch (err) {
      setError('Error deleting player');
      console.error(err);
    } finally {
      setDeleting(false);
    }
  };

  return (
    <Container className="my-4">
      <h2 className="mb-3">Players</h2>

      {error && <Alert variant="danger">{error}</Alert>}

      {/* Search */}
      <InputGroup className="mb-3">
        <InputGroup.Text>
          <i className="bi bi-search"></i>
        </InputGroup.Text>
        <Form.Control
          placeholder="Search by name, CI or faculty..."
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
              <th>CI</th>
              <th>Name</th>
              <th>Faculty</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredPlayers.length === 0 ? (
              <tr>
                <td colSpan={5} className="text-center">
                  No players found
                </td>
              </tr>
            ) : (
              filteredPlayers.map((player) => (
                <tr key={player.player_id}>
                  <td>{player.player_id}</td>
                  <td>{player.CI}</td>
                  <td>{player.name}</td>
                  <td>{player.faculty}</td>
                  <td>
                    <Button
                      variant="danger"
                      size="sm"
                      onClick={() => setDeleteId(player.player_id)}
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
        <Modal.Body>Are you sure you want to delete this player?</Modal.Body>
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
