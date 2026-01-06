'use client';
import { Card, Row, Col, Container, Button } from 'react-bootstrap';

const news = [
  {
    title: "🎾 Torneo Interfacultades de Tenis 2024",
    description: "La Facultad de Contabilidad lidera el cuadro de honor tras imponerse en dobles mixtos. Inscripciones abiertas hasta el 15 de diciembre.",
    image: "/static/images/tenis.jpg",
    link: "#"
  },
  {
    title: "♟️ Campeonato de Ajedrez Rápido",
    description: "Estudiantes de Contabilidad demuestran habilidades estratégicas en el torneo interdepartamental. Gran maestro internacional como invitado especial.",
    image: "/static/images/ajedrez.jpg",
    link: "#"
  },
  {
    title: "📊 Feria de Prácticas en Contabilidad",
    description: "Las Big Four visitan la facultad para reclutar talento. Talleres sobre nuevas normas IFRS y oportunidades de certificación CPA.",
    image: "/static/images/confin.jpg",
    link: "#"
  }
];

export default function NewsGrid() {
  return (
    <Container className="my-5">
      <h2 className="mb-4 text-center">Noticias Universitarias</h2>
      <Row className="g-4">
        {news.map((item, idx) => (
          <Col md={4} key={idx}>
            <Card className="h-100">
              <Card.Img variant="top" src={item.image} />
              <Card.Body className="d-flex flex-column">
                <Card.Title>{item.title}</Card.Title>
                <Card.Text className="flex-grow-1">{item.description}</Card.Text>
                <Button href={item.link} variant="danger" className="mt-auto">Ver detalles</Button>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </Container>
  );
}
