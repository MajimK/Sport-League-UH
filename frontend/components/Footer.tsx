'use client'
import { Container, Row, Col } from 'react-bootstrap';

export default function Footer() {
    const uhRed = '#6D222E';
    const uhGold = '#D4AF37';

    return (
        <footer style={{ backgroundColor: uhRed, color: 'white', padding: '30px 0 10px' }}>
            <Container>
                <Row className="mb-3">
                    <Col md={4}>
                        <h5 style={{ color: uhGold }}>Contacto</h5>
                        <p>Email: deporte@uh.cu</p>
                        <p>Teléfonos: +53 7 xxx xxxx</p>
                    </Col>
                    <Col md={4}>
                        <h5 style={{ color: uhGold }}>Enlaces Rápidos</h5>
                        <ul className="list-unstyled">
                            <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Reglamento General</a></li>
                            <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Archivo Histórico</a></li>
                            <li><a href="#" style={{ color: 'white', textDecoration: 'none' }}>Comité Organizador</a></li>
                        </ul>
                    </Col>
                    <Col md={4}>
                        <h5 style={{ color: uhGold }}>Síguenos</h5>
                        <a href="#" style={{ color: 'white', marginRight: '10px' }}><i className="fab fa-facebook-f"></i></a>
                        <a href="#" style={{ color: 'white', marginRight: '10px' }}><i className="fab fa-instagram"></i></a>
                        <a href="#" style={{ color: 'white' }}><i className="fab fa-youtube"></i></a>
                    </Col>
                </Row>
                <Row>
                    <Col className="text-center">
                        <p>&copy; 2025 Deporte UH. Todos los derechos reservados.</p>
                    </Col>
                </Row>
            </Container>
        </footer>
    );
}
