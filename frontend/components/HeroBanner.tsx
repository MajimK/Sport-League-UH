'use client';

import { useState, useEffect } from 'react';

const images = [
  '/static/images/banner_bg.jpg',
  '/static/images/tenis.jpg',
  '/static/images/ajedrez.jpg',
  '/static/images/confin.jpg'
];

export default function HeroBanner() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [nextIndex, setNextIndex] = useState(1);
  const [opacity, setOpacity] = useState(1);

  useEffect(() => {
    const interval = setInterval(() => {
      // Iniciar fade out
      setOpacity(0);
      
      // Cuando fade out termina (500ms)
      setTimeout(() => {
        // Cambiar índices
        setCurrentIndex(nextIndex);
        setNextIndex((nextIndex + 1) % images.length);
        
        // Opacidad vuelve inmediatamente a 1 (sin transición)
        setOpacity(1);
      }, 500);
    }, 5000);

    return () => clearInterval(interval);
  }, [nextIndex]);

  const handleDotClick = (index: number) => {
    setOpacity(0);
    setTimeout(() => {
      setCurrentIndex(index);
      setNextIndex((index + 1) % images.length);
      setOpacity(1);
    }, 500);
  };

  return (
    <section style={{
      position: 'relative',
      height: '400px',
      overflow: 'hidden'
    }}>
      {/* Fondo: siempre muestra la siguiente imagen */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundImage: `url(${images[nextIndex]})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center'
      }} />
      
      {/* Frente: imagen actual con fade out */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundImage: `url(${images[currentIndex]})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        opacity: opacity,
        transition: opacity === 0 ? 'opacity 0.5s ease-in-out' : 'none'
      }} />
      
      {/* Overlay */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0,0,0,0.4)'
      }} />
      
      <div style={{
        position: 'relative',
        zIndex: 2,
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: 'white',
        textAlign: 'center'
      }}>
        <h1 style={{ fontSize: '3rem' }}>Movimiento Deportivo Universitario</h1>
      </div>
      
      <div style={{
        position: 'absolute',
        bottom: '20px',
        left: '0',
        right: '0',
        display: 'flex',
        justifyContent: 'center',
        gap: '10px',
        zIndex: 3
      }}>
        {images.map((_, index) => (
          <button
            key={index}
            onClick={() => handleDotClick(index)}
            style={{
              width: '12px',
              height: '12px',
              borderRadius: '50%',
              border: '2px solid white',
              backgroundColor: index === currentIndex ? 'white' : 'transparent',
              cursor: 'pointer'
            }}
          />
        ))}
      </div>
    </section>
  )
}