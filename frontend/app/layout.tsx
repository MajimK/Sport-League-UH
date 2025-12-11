import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Caribe | Portal Oficial',
  description: 'Portal deportivo universitario',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="es">
      <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
      </head>
      <body className={inter.className}>
        <header className="main-header">
          <div className="header-top">
            <div className="logos">
          <div style={{ 
            display: 'flex', 
            alignItems: 'center',
            gap: '10px'
          }}>
            {/* Logo del indio - REEMPLAZAR CON IMAGEN REAL */}
            <img 
              src="/static/images/indio-logo.png" 
              alt="Logo Indio Caribe" 
              style={{
                width: '50px',
                height: '50px',
                objectFit: 'contain'
              }}
            />
            <span className="site-title">CARIBE</span>
          </div>
        </div>
          </div>
          <nav className="main-nav">
            <ul>
              <li><a href="/">Inicio</a></li>
              <li><a href="#noticias">Noticias</a></li>
              <li className="dropdown">
                <a href="#movimiento" className="dropdown-toggle">
                  Movimiento Deportivo <i className="fas fa-caret-down"></i>
                </a>
                <div className="dropdown-content">
                  <a href="#deportes">Deportes</a>
                  <a href="#resultados">Resultados</a>
                  <a href="#calendario">Calendario</a>
                </div>
              </li>
              <li className="dropdown">
                <a href="#nosotros" className="dropdown-toggle">
                  Nosotros <i className="fas fa-caret-down"></i>
                </a>
                <div className="dropdown-content">
                  <a href="#multimedia">Multimedia</a>
                  <a href="#historia">Historia</a>
                </div>
              </li>
            </ul>
          </nav>
        </header>
        {children}
        <footer className="main-footer">
          <div className="footer-grid container">
            <div className="footer-column">
              <h4>Contacto</h4>
              <p>Email: deporte@uh.cu</p>
            </div>
            <div className="footer-column">
              <h4>Enlaces Rápidos</h4>
              <ul>
                <li><a href="#">Reglamento General</a></li>
                <li><a href="https://www.uh.cu">Universidad de La Habana</a></li>
                <li><a href="#">Comité Organizador</a></li>
              </ul>
            </div>
            <div className="footer-column social">
              <h4>Síguenos</h4>
              <a href="#"><i className="fab fa-facebook-f"></i></a>
              <a href="#"><i className="fab fa-instagram"></i></a>
              <a href="#"><i className="fab fa-telegram"></i></a>
              <a href="#"><i className="fab fa-whatsapp"></i></a>
            </div>
          </div>
          <div className="footer-bottom">
            <p>&copy; 2025 Caribe. Todos los derechos reservados.</p>
          </div>
        </footer>
      </body>
    </html>
  )
}