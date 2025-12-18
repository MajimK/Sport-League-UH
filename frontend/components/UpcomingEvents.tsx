'use client';
import { Card, Col, Row, Container, Button } from 'react-bootstrap';

const events = [
  { sport: "Baloncesto", date: "Hoy, 16:00h", teams: "Informática vs. Derecho", location: "Polideportivo Central" },
  { sport: "Fútbol", date: "Miércoles, 10:30h", teams: "FEU vs. Voluntarios", location: "Campo #3" }
];

export default function UpcomingEvents() {
  return (
    <Container className="my-5">
      <h2 className="mb-4 text-center">Próximos Eventos</h2>
      <Row className="g-4">
        {events.map((event, idx) => (
          <Col md={6} key={idx}>
            <Card className="h-100">
              <Card.Body>
                <Card.Title>{event.sport}</Card.Title>
                <Card.Subtitle className="mb-2 text-danger">{event.date}</Card.Subtitle>
                <Card.Text>{event.teams}</Card.Text>
                <Card.Text><i className="fas fa-map-marker-alt"></i> {event.location}</Card.Text>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
      <div className="text-center mt-4">
        <Button href="#calendario" variant="outline-primary">Ver calendario completo</Button>
      </div>
    </Container>
  );
}
