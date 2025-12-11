'use client';

import { useState, useEffect } from 'react';

interface Player {
  player_id: number;
  name: string;
  CI: string;
  faculty: string;
  teams?: Team[]; // Equipos a los que pertenece
}

interface Team {
  team_id: number;
  name: string;
  description: string;
}

export default function PlayersPage() {
  const [players, setPlayers] = useState<Player[]>([]);
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [filterFaculty, setFilterFaculty] = useState('');

  useEffect(() => {
    fetchPlayers();
  }, []);

  const fetchPlayers = async () => {
    try {
      const [playersRes, teamsRes] = await Promise.all([
        fetch('http://localhost:5000/admin/players/'),
        fetch('http://localhost:5000/admin/teams/')
      ]);

      if (!playersRes.ok || !teamsRes.ok) throw new Error('Failed to fetch data');

      const playersData: Player[] = await playersRes.json();
      const teamsData: Team[] = await teamsRes.json();

      // Obtener equipos para cada jugador
      const playersWithTeams = await Promise.all(
        playersData.map(async (player) => {
          try {
            const teamsRes = await fetch(`http://localhost:5000/admin/players/${player.player_id}/teams`);
            if (teamsRes.ok) {
              const playerTeams = await teamsRes.json();
              return { ...player, teams: playerTeams };
            }
            return { ...player, teams: [] };
          } catch {
            return { ...player, teams: [] };
          }
        })
      );

      setPlayers(playersWithTeams);
      setTeams(teamsData);
    } catch (err) {
      setError('Error loading data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Filtrar jugadores
  const filteredPlayers = players.filter(player => {
    const matchesSearch = searchTerm === '' || 
      player.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      player.CI.toLowerCase().includes(searchTerm.toLowerCase()) ||
      player.faculty.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesFaculty = filterFaculty === '' || 
      player.faculty === filterFaculty;
    
    return matchesSearch && matchesFaculty;
  });

  // Obtener facultades únicas para filtro
  const uniqueFaculties = Array.from(new Set(players.map(p => p.faculty))).filter(Boolean);

  if (loading) return (
    <div className="container mt-4 text-center">
      <div className="spinner-border text-primary" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
      <p className="mt-2">Cargando jugadores...</p>
    </div>
  );

  if (error) return (
    <div className="container mt-4">
      <div className="alert alert-danger">{error}</div>
    </div>
  );

  return (
    <div className="container mt-4">
      <h1 className="mb-4">Jugadores del Caribe</h1>
      
      {/* Filtros */}
      <div className="card mb-4">
        <div className="card-body">
          <div className="row">
            <div className="col-md-6">
              <div className="form-group mb-3">
                <label htmlFor="search" className="form-label">Buscar jugador</label>
                <input
                  type="text"
                  id="search"
                  className="form-control"
                  placeholder="Buscar por nombre, CI o facultad..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
            </div>
            <div className="col-md-6">
              <div className="form-group mb-3">
                <label htmlFor="faculty" className="form-label">Filtrar por facultad</label>
                <select
                  id="faculty"
                  className="form-control"
                  value={filterFaculty}
                  onChange={(e) => setFilterFaculty(e.target.value)}
                >
                  <option value="">Todas las facultades</option>
                  {uniqueFaculties.map(faculty => (
                    <option key={faculty} value={faculty}>{faculty}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>
          <div className="d-flex justify-content-between align-items-center">
            <span className="text-muted">
              {filteredPlayers.length} de {players.length} jugadores
            </span>
            <button 
              className="btn btn-outline-primary"
              onClick={fetchPlayers}
            >
              <i className="fas fa-sync-alt"></i> Actualizar
            </button>
          </div>
        </div>
      </div>

      {/* Lista de jugadores */}
      <div className="row">
        {filteredPlayers.length === 0 ? (
          <div className="col-12">
            <div className="alert alert-info text-center">
              No se encontraron jugadores
            </div>
          </div>
        ) : (
          filteredPlayers.map(player => (
            <div key={player.player_id} className="col-md-6 col-lg-4 mb-4">
              <div className="card h-100">
                <div className="card-body">
                  <div className="d-flex justify-content-between align-items-start mb-3">
                    <h5 className="card-title mb-0">{player.name}</h5>
                    <span className="badge bg-primary">ID: {player.player_id}</span>
                  </div>
                  
                  <div className="mb-3">
                    <p className="mb-1">
                      <i className="fas fa-id-card text-muted me-2"></i>
                      <strong>CI:</strong> {player.CI}
                    </p>
                    <p className="mb-1">
                      <i className="fas fa-university text-muted me-2"></i>
                      <strong>Facultad:</strong> {player.faculty}
                    </p>
                  </div>

                  {/* Equipos */}
                  <div className="mb-3">
                    <h6 className="border-bottom pb-2">
                      <i className="fas fa-users me-2"></i>
                      Equipos ({player.teams?.length || 0})
                    </h6>
                    {player.teams && player.teams.length > 0 ? (
                      <div className="d-flex flex-wrap gap-2">
                        {player.teams.map(team => (
                          <span 
                            key={team.team_id}
                            className="badge bg-secondary"
                            style={{ cursor: 'pointer' }}
                            title={team.description}
                          >
                            {team.name}
                          </span>
                        ))}
                      </div>
                    ) : (
                      <p className="text-muted small mb-0">No pertenece a ningún equipo</p>
                    )}
                  </div>

                  {/* Acciones */}
                  <div className="d-flex justify-content-end gap-2">
                    <button 
                      className="btn btn-sm btn-outline-primary"
                      onClick={() => {
                        // Navegar a página del jugador (si existe)
                        console.log('Ver perfil de:', player.player_id);
                      }}
                    >
                      <i className="fas fa-eye"></i> Ver
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Vista de tabla alternativa */}
      <div className="card mt-4">
        <div className="card-header">
          <h5 className="mb-0">Vista de tabla</h5>
        </div>
        <div className="card-body p-0">
          <div className="table-responsive">
            <table className="table table-hover mb-0">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Nombre</th>
                  <th>CI</th>
                  <th>Facultad</th>
                  <th>Equipos</th>
                </tr>
              </thead>
              <tbody>
                {filteredPlayers.slice(0, 10).map(player => (
                  <tr key={player.player_id}>
                    <td>{player.player_id}</td>
                    <td>{player.name}</td>
                    <td>{player.CI}</td>
                    <td>{player.faculty}</td>
                    <td>
                      {player.teams && player.teams.length > 0 ? (
                        <div>
                          {player.teams.map(team => (
                            <div key={team.team_id} className="small">
                              {team.name}
                            </div>
                          ))}
                        </div>
                      ) : (
                        <span className="text-muted">Sin equipo</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}