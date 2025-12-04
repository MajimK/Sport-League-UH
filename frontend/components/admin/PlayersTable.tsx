'use client';

import { useState } from 'react';

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
        credentials: 'include'
      });

      if (!response.ok) throw new Error('Failed to delete player');

      onSuccess();
    } catch (err) {
      setError('Error deleting player');
      console.error(err);
    } finally {
      setDeleting(false);
      setDeleteId(null);
    }
  };

  return (
    <div className="card">
      <div className="card-body">
        <h2 className="card-title">Existing Players</h2>
        
        {error && <div className="alert alert-danger">{error}</div>}
        
        <div className="table-responsive">
          <table className="table table-striped">
            <thead>
              <tr>
                <th>ID</th>
                <th>CI</th>
                <th>Name</th>
                <th>Faculty</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {players.length === 0 ? (
                <tr>
                  <td colSpan={5} className="text-center">No players found</td>
                </tr>
              ) : (
                players.map(player => (
                  <tr key={player.player_id}>
                    <td>{player.player_id}</td>
                    <td>{player.CI}</td>
                    <td>{player.name}</td>
                    <td>{player.faculty}</td>
                    <td>
                      <div className="btn-group btn-group-sm">
                        <button
                          className="btn btn-danger"
                          onClick={() => setDeleteId(player.player_id)}
                          title="Delete"
                        >
                          <i className="fas fa-trash"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Delete Modal */}
      {deleteId && (
        <div className="modal show d-block" tabIndex={-1} style={{backgroundColor: 'rgba(0,0,0,0.5)'}}>
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Confirm Delete</h5>
                <button 
                  type="button" 
                  className="btn-close"
                  onClick={() => setDeleteId(null)}
                  disabled={deleting}
                ></button>
              </div>
              <div className="modal-body">
                Are you sure you want to delete this player?
              </div>
              <div className="modal-footer">
                <button 
                  type="button" 
                  className="btn btn-secondary"
                  onClick={() => setDeleteId(null)}
                  disabled={deleting}
                >
                  Cancel
                </button>
                <button 
                  type="button" 
                  className="btn btn-danger"
                  onClick={handleDelete}
                  disabled={deleting}
                >
                  {deleting ? 'Deleting...' : 'Delete'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}