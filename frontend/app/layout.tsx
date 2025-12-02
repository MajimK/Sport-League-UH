import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Deporte UH | Portal Oficial de la Universidad de La Habana',
  description: 'Movimiento Deportivo Universitario',
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
              <span className="site-title">DEPORTE <span className="uh">UH</span></span>
            </div>
          </div>
          <nav className="main-nav">
            <ul>
              <li><a href="#">Inicio</a></li>
              <li><a href="#noticias">Noticias</a></li>
              <li><a href="#eventos">Eventos Deportivos</a></li>
              <li><a href="#deportes">Deportes</a></li>
              <li><a href="#resultados">Resultados</a></li>
              <li><a href="#calendario">Calendario</a></li>
              <li><a href="#multimedia">Multimedia</a></li>
              <li><a href="#nosotros">Nosotros</a></li>
              <li><a href="#historia">Historia</a></li>
            </ul>
          </nav>
        </header>
        {children}
        <footer className="main-footer">
          <div className="footer-grid container">
            <div className="footer-column">
              <h4>Contacto</h4>
              <p>Email: deporte@uh.cu</p>
              <p>Teléfonos: +53 7 xxx xxxx</p>
            </div>
            <div className="footer-column">
              <h4>Enlaces Rápidos</h4>
              <ul>
                <li><a href="#">Reglamento General</a></li>
                <li><a href="#">Archivo Histórico</a></li>
                <li><a href="#">Comité Organizador</a></li>
              </ul>
            </div>
            <div className="footer-column social">
              <h4>Síguenos</h4>
              <a href="#"><i className="fab fa-facebook-f"></i></a>
              <a href="#"><i className="fab fa-instagram"></i></a>
              <a href="#"><i className="fab fa-youtube"></i></a>
            </div>
          </div>
          <div className="footer-bottom">
            <p>&copy; 2025 Deporte UH. Todos los derechos reservados.</p>
          </div>
        </footer>
      </body>
    </html>
  )
}