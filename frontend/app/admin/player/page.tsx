'use client';

import { useState, useEffect } from 'react';
import { Container, Row, Col, Button, Form, ListGroup, Card, Alert } from 'react-bootstrap';

type Gender = 'Masculino' | 'Femenino';

export default function ManagePlayersPage() {
  const [ci, setCi] = useState('');
  const [sport, setSport] = useState('');
  const [gender, setGender] = useState<Gender>('Masculino');
  const [error, setError] = useState<string | null>(null);
  const [pendingPlayers, setPendingPlayers] = useState<
  { ci: string; sport: string; gender: Gender; name: string; faculty: string }[]
>([]);

  // Simular datos del backend (solo para UI)
  const fetchPlayerData = async (ci: string) => {
    // TODO: Descomentar e implementar cuando el backend esté listo
    /*
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/players/${ci}`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
      });
      if (!response.ok) throw new Error('Player not found');
      const data = await response.json();
      return { name: data.name, faculty: data.faculty, gender: data.gender };
    } catch (err) {
      console.error('Failed to fetch player:', err);
      throw err;
    }
    */

    // Placeholder temporal (solo para mostrar en UI)
    return { name: 'Nombre Placeholder', faculty: 'Facultad Placeholder' };
  };

  const validateAndAdd = async () => {
    setError(null);

    if (!/^\d{11}$/.test(ci)) {
      setError('El Carnet de Identidad debe tener exactamente 11 dígitos numéricos.');
      return;
    }

    const penultimateDigit = parseInt(ci.charAt(9), 10);
    if (gender === 'Masculino' && penultimateDigit % 2 !== 0) {
      setError('El CI no corresponde a sexo masculino (penúltimo dígito debe ser par).');
      return;
    }
    if (gender === 'Femenino' && penultimateDigit % 2 === 0) {
      setError('El CI no corresponde a sexo femenino (penúltimo dígito debe ser impar).');
      return;
    }

    if (!sport.trim()) {
      setError('El campo "Deporte" es obligatorio.');
      return;
    }

    // Fetch simulado (reemplazará al placeholder)
    let name = 'Nombre Placeholder';
    let faculty = 'Facultad Placeholder';
    try {
      const data = await fetchPlayerData(ci);
      name = data.name;
      faculty = data.faculty;
    } catch {
      // En caso de error real, podrías usar placeholders o bloquear
    }

    setPendingPlayers([
      ...pendingPlayers,
      { ci, sport: sport.trim(), gender, name, faculty },
    ]);
    setCi('');
    setSport('');
    setGender('Masculino');
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      validateAndAdd();
    }
  };

  return (
    <Container className="mt-4">
      <h1 className="mb-4" style={{ color: 'var(--color-uh-red)' }}>
        Manage Players
      </h1>

      <Row className="g-4">
        {/* Left: Add Player */}
        <Col md={6}>
          <Card>
            <Card.Body>
              <Card.Title>Add Player</Card.Title>
              {error && <Alert variant="danger">{error}</Alert>}
              <Form>
                <Form.Group className="mb-3">
                  <Form.Label>Carnet de Identidad (CI)</Form.Label>
                  <Form.Control
                    type="text"
                    value={ci}
                    onChange={(e) => setCi(e.target.value.replace(/\D/g, '').slice(0, 11))}
                    onKeyDown={handleKeyDown}
                    placeholder="11 dígitos numéricos"
                    maxLength={11}
                  />
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Deporte</Form.Label>
                  <Form.Control
                    type="text"
                    value={sport}
                    onChange={(e) => setSport(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ej: Volleyball"
                  />
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Sexo</Form.Label>
                  <Form.Select
                    value={gender}
                    onChange={(e) => setGender(e.target.value as Gender)}
                  >
                    <option value="Masculino">Masculino</option>
                    <option value="Femenino">Femenino</option>
                  </Form.Select>
                </Form.Group>

                <Button
                  variant="primary"
                  onClick={validateAndAdd}
                  disabled={!/^\d{11}$/.test(ci) || !sport.trim()}
                >
                  Agregar
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>

        {/* Right: Pending Players List */}
        <Col md={6}>
          <Card>
            <Card.Body>
              <Card.Title>Pending Players ({pendingPlayers.length})</Card.Title>
              {pendingPlayers.length === 0 ? (
                <p className="text-muted">No players added yet.</p>
              ) : (
                <ListGroup>
                  {pendingPlayers.map((player, index) => (
                    <ListGroup.Item key={index}>
                      <strong>CI:</strong> {player.ci} — <strong>Nombre:</strong> {player.name} —{' '}
                      <strong>Facultad:</strong> {player.faculty} — <strong>Deporte:</strong> {player.sport} —{' '}
                      <strong>Sexo:</strong> {player.gender}
                    </ListGroup.Item>
                  ))}
                </ListGroup>
              )}
              <Button
                variant="success"
                className="mt-3"
                disabled={pendingPlayers.length === 0}
                // TODO: conectar con backend para registrar todos
              >
                Registrar Jugadores
              </Button>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}