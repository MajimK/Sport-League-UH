'use client';

import { useState } from 'react';
import { Container, Row, Col, Button, Form, ListGroup, Card, Alert, InputGroup } from 'react-bootstrap';

export default function ManageUsersPage() {
  // Form state
  const [email, setEmail] = useState('');
  const [nickname, setNickname] = useState('');
  const [password, setPassword] = useState('');
  const [faculty, setFaculty] = useState('');
  const [error, setError] = useState<string | null>(null);

  // Mock user list (placeholders)
  const [users] = useState([
    { id: 1, email: 'admin@example.com', nickname: 'admin', faculty: 'Informática' },
    { id: 2, email: 'manager@uh.cu', nickname: 'manager_uh', faculty: 'Matemática' },
    { id: 3, email: 'user@test.cu', nickname: 'test_user', faculty: 'Física' },
  ]);

  const [searchTerm, setSearchTerm] = useState('');

  const handleAdd = () => {
    setError(null);

    if (!email.trim() || !nickname.trim() || !password.trim() || !faculty.trim()) {
      setError('All fields are required.');
      return;
    }

    if (!/^\S+@\S+\.\S+$/.test(email)) {
      setError('Please enter a valid email.');
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters long.');
      return;
    }

    // TODO: call backend to create user
    console.log('New user:', { email, nickname, password, faculty });
    alert('User added (placeholder logic).');

    // Reset form
    setEmail('');
    setNickname('');
    setPassword('');
    setFaculty('');
  };

  const filteredUsers = users.filter(
    (user) =>
      user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.nickname.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.faculty.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <Container className="mt-4">
      <h1 className="mb-4" style={{ color: 'var(--color-uh-red)' }}>
        Manage Users
      </h1>

      <Row className="g-4">
        {/* Left: Add User Form */}
        <Col md={6}>
          <Card>
            <Card.Body>
              <Card.Title>Add New User</Card.Title>
              {error && <Alert variant="danger">{error}</Alert>}
              <Form>
                <Form.Group className="mb-3">
                  <Form.Label>Email</Form.Label>
                  <Form.Control
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="user@example.com"
                  />
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Nickname</Form.Label>
                  <Form.Control
                    type="text"
                    value={nickname}
                    onChange={(e) => setNickname(e.target.value)}
                    placeholder="john_doe"
                  />
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Password</Form.Label>
                  <Form.Control
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                  />
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Facultad</Form.Label>
                  <Form.Control
                    type="text"
                    value={faculty}
                    onChange={(e) => setFaculty(e.target.value)}
                    placeholder="Ej: Informática"
                  />
                </Form.Group>

                <Button variant="primary" onClick={handleAdd} disabled={!email || !nickname || !password || !faculty}>
                  Add User
                </Button>
              </Form>
            </Card.Body>
          </Card>
        </Col>

        {/* Right: Users List with Search */}
        <Col md={6}>
          <Card>
            <Card.Body>
              <Card.Title>Users ({filteredUsers.length})</Card.Title>

              <InputGroup className="mb-3">
                <Form.Control
                  placeholder="Search by email, nickname or faculty..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
                <Button variant="outline-secondary" onClick={() => setSearchTerm('')}>
                  Clear
                </Button>
              </InputGroup>

              {filteredUsers.length === 0 ? (
                <p className="text-muted">No users found.</p>
              ) : (
                <ListGroup>
                  {filteredUsers.map((user) => (
                    <ListGroup.Item key={user.id} className="d-flex justify-content-between align-items-center">
                      <div>
                        <strong>{user.nickname}</strong> — {user.email} <br />
                        <small className="text-muted">Facultad: {user.faculty}</small>
                      </div>
                      <div>
                        <Button variant="warning" size="sm" className="me-1">
                          Edit
                        </Button>
                        <Button variant="danger" size="sm">
                          Delete
                        </Button>
                      </div>
                    </ListGroup.Item>
                  ))}
                </ListGroup>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}