'use client';
import { Carousel, Container } from 'react-bootstrap';

const images = [
  { src: '/static/images/banner_bg.jpg', alt: 'Banner UH' },
  { src: '/static/images/tenis.jpg', alt: 'Tenis' },
  { src: '/static/images/ajedrez.jpg', alt: 'Ajedrez' },
  { src: '/static/images/confin.jpg', alt: 'Feria de Contabilidad' },
];

export default function HeroBanner() {
  return (
    <Carousel fade interval={5000}>
      {images.map((img, index) => (
        <Carousel.Item key={index}>
          <div
            style={{
              height: '400px',
              backgroundImage: `url(${img.src})`,
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              position: 'relative',
            }}
          >
            <div
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                backgroundColor: 'rgba(0,0,0,0.4)',
              }}
            />
            <Container
              style={{
                position: 'relative',
                height: '100%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
                textAlign: 'center',
              }}
            >
              <h1 className="display-4">Movimiento Deportivo Universitario</h1>
            </Container>
          </div>
        </Carousel.Item>
      ))}
    </Carousel>
  );
}
