'use client'
import { Navbar, Nav, Container, NavDropdown } from 'react-bootstrap';

export default function Header() {
    const uhRed = '#6D222E';
    const uhGold = '#D4AF37';

    // Estilos para links y títulos de dropdown
    const navLinkStyle = {
        color: 'white',
        backgroundColor: uhRed,
        borderRadius: '0.25rem',
        margin: '0 2px',
        transition: '0.3s',
    };

    const handleMouseOver = (e: React.MouseEvent<HTMLAnchorElement | HTMLSpanElement>) => {
        e.currentTarget.style.backgroundColor = uhGold;
        e.currentTarget.style.color = uhRed;
    };

    const handleMouseOut = (e: React.MouseEvent<HTMLAnchorElement | HTMLSpanElement>) => {
        e.currentTarget.style.backgroundColor = uhRed;
        e.currentTarget.style.color = 'white';
    };

    return (
        <>
            {/* Barra superior blanca con logo */}
            <div style={{ backgroundColor: 'white', padding: '5px 0' }}>
                <Container className="d-flex align-items-center">
                    <img src="/static/images/Logo_Caribe_57_negro.png" alt="Logo UH" height={50} />
                    <span style={{ marginLeft: '10px', fontWeight: 700, fontSize: '1.5rem', color: uhRed }}>
                        DEPORTE <span style={{ color: uhGold }}>UH</span>
                    </span>
                </Container>
            </div>

            {/* Barra de navegación roja */}
            <Navbar expand="lg" style={{ backgroundColor: uhRed }} variant="dark">
                <Container>
                    <Navbar.Toggle aria-controls="navbar-nav" />
                    <Navbar.Collapse id="navbar-nav">
                        <Nav className="ms-auto">
                            <Nav.Link
                                href="/"
                                style={navLinkStyle}
                                onMouseOver={handleMouseOver}
                                onMouseOut={handleMouseOut}
                            >
                                Inicio
                            </Nav.Link>
                            <Nav.Link
                                href="#noticias"
                                style={navLinkStyle}
                                onMouseOver={handleMouseOver}
                                onMouseOut={handleMouseOut}
                            >
                                Noticias
                            </Nav.Link>

                            {/* Dropdown Consulte */}
                            <NavDropdown
                                title={
                                    <span style={navLinkStyle} onMouseOver={handleMouseOver} onMouseOut={handleMouseOut}>
                                        Consulte
                                    </span>
                                }
                                id="dropdown-movimiento"
                                menuVariant="dark"
                            >
                                <NavDropdown.Item
                                    href="/user/players"
                                    style={{ ...navLinkStyle, margin: 0 }}
                                    onMouseOver={handleMouseOver}
                                    onMouseOut={handleMouseOut}
                                >
                                    Tabla de Jugadores
                                </NavDropdown.Item>
                                <NavDropdown.Item
                                    href="/user/teams"
                                    style={{ ...navLinkStyle, margin: 0 }}
                                    onMouseOver={handleMouseOver}
                                    onMouseOut={handleMouseOut}
                                >
                                    Tabla de Equipos
                                </NavDropdown.Item>
                            </NavDropdown>
                            <NavDropdown
                                title={
                                    <span style={navLinkStyle} onMouseOver={handleMouseOver} onMouseOut={handleMouseOut}>
                                        Movimiento Deportivo
                                    </span>
                                }
                                id="dropdown-movimiento"
                                menuVariant="dark"
                            >
                                <NavDropdown.Item
                                    href="#calendario"
                                    style={{ ...navLinkStyle, margin: 0 }}
                                    onMouseOver={handleMouseOver}
                                    onMouseOut={handleMouseOut}
                                >
                                    Calendario
                                </NavDropdown.Item>
                                <NavDropdown.Item
                                    href="#resultados"
                                    style={{ ...navLinkStyle, margin: 0 }}
                                    onMouseOver={handleMouseOver}
                                    onMouseOut={handleMouseOut}
                                >
                                    Resultados
                                </NavDropdown.Item>
                                <NavDropdown.Item
                                    href="#deportes"
                                    style={{ ...navLinkStyle, margin: 0 }}
                                    onMouseOver={handleMouseOver}
                                    onMouseOut={handleMouseOut}
                                >
                                    Deportes
                                </NavDropdown.Item>
                            </NavDropdown>

                            <NavDropdown
                                title={
                                    <span style={navLinkStyle} onMouseOver={handleMouseOver} onMouseOut={handleMouseOut}>
                                        Nosotros
                                    </span>
                                }
                                id="dropdown-nosotros"
                                menuVariant="dark"
                            >
                                <NavDropdown.Item
                                    href="#historia"
                                    style={{ ...navLinkStyle, margin: 0 }}
                                    onMouseOver={handleMouseOver}
                                    onMouseOut={handleMouseOut}
                                >
                                    Historia
                                </NavDropdown.Item>
                                <NavDropdown.Item
                                    href="#multimedia"
                                    style={{ ...navLinkStyle, margin: 0 }}
                                    onMouseOver={handleMouseOver}
                                    onMouseOut={handleMouseOut}
                                >
                                    Multimedia
                                </NavDropdown.Item>
                            </NavDropdown>

                            <Nav.Link
                                href="/login"
                                style={navLinkStyle}
                                onMouseOver={handleMouseOver}
                                onMouseOut={handleMouseOut}
                            >
                                <i className="fas fa-sign-in-alt"></i> Login
                            </Nav.Link>
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
        </>
    );
}
