'use client';

import Link from 'next/link';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';

export default function AdminDashboard() {
    return (
        <Container className="mt-4">

            {/* Header */}
            <div className="d-flex justify-content-between align-items-center mb-4">
                <h1 className="fw-bold" style={{ color: 'var(--color-uh-red)' }}>
                    Admin Panel
                </h1>
                <Link href="/logout" passHref>
                    <Button variant="outline-danger" size="sm">Logout</Button>
                </Link>
            </div>

            <Row>

                {/* Main Content */}
                <Col md={9}>
                    <Card className="shadow-sm mb-4">
                        <Card.Body>
                            <h2 className="fw-semibold">Welcome to the Admin Dashboard</h2>
                            <p className="text-muted">
                                Use the modules below to manage the system quickly.
                            </p>
                        </Card.Body>
                    </Card>

                    {/* Quick Action Cards */}
                    <Row className="g-4">

                        {/* Teams Card */}
                        <Col md={6}>
                            <Card className="shadow-sm h-100">
                                <Card.Body>
                                    <h4 className="fw-bold d-flex align-items-center mb-3">
                                        <i className="bi bi-people-fill text-primary me-2"></i>
                                        Teams
                                    </h4>
                                    <p className="text-muted">
                                        Create, edit and delete teams in the system.
                                    </p>
                                    <Link href="/admin/team" passHref>
                                        <Button variant="primary">Manage Teams</Button>
                                    </Link>
                                </Card.Body>
                            </Card>
                        </Col>

                        {/* Players Card */}
                        <Col md={6}>
                            <Card className="shadow-sm h-100">
                                <Card.Body>
                                    <h4 className="fw-bold d-flex align-items-center mb-3">
                                        <i className="bi bi-person-fill text-success me-2"></i>
                                        Players
                                    </h4>
                                    <p className="text-muted">
                                        Add players, update info or remove records.
                                    </p>
                                    <Link href="/admin/player" passHref>
                                        <Button variant="success">Manage Players</Button>
                                    </Link>
                                </Card.Body>
                            </Card>
                        </Col>

                        {/* Puedes agregar más tarjetas aquí */}

                    </Row>
                </Col>
            </Row>
        </Container>
    );
}
