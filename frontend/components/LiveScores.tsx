'use client';
import { Container, Badge, Button, Stack } from 'react-bootstrap';

export default function LiveScores() {
  return (
    <section style={{ backgroundColor: '#343a40', color: 'white', padding: '1rem 0' }}>
      <Container>
        <Stack direction="horizontal" gap={3} className="flex-wrap justify-content-center">
          <Badge bg="danger"><i className="fas fa-tennis-ball"></i> Tenis: Contabilidad 3 - 2 Economía</Badge>
          <Badge bg="warning" text="dark"><i className="fas fa-chess"></i> Ajedrez: F. Contabilidad vs Matemática (En juego)</Badge>
          <Badge bg="success"><i className="fas fa-medal"></i> Medallero: 1.º Contabilidad | 2.º Matemática | 3.º Economía</Badge>
          <Button href="#resultados" variant="outline-light">Ver todos los resultados</Button>
        </Stack>
      </Container>
    </section>
  );
}
