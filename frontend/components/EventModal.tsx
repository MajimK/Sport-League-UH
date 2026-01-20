// frontend/components/EventModal.tsx
'use client';

import { ReactNode } from 'react';

interface EventModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode; // para la descripción u otros contenidos
}

export default function EventModal({ isOpen, onClose, title, children }: EventModalProps) {
  if (!isOpen) return null;

  return (
    <>
      {/* Fondo oscuro */}
      <div
        className="modal-backdrop fade show"
        style={{ backgroundColor: 'rgba(0, 0, 0, 0.5)', position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', zIndex: 1050 }}
        onClick={onClose}
      />

      {/* Ventana modal */}
      <div
        className="modal d-block"
        style={{ zIndex: 1051 }}
        onClick={e => e.stopPropagation()} // Evita cerrar al hacer clic dentro
      >
        <div className="modal-dialog modal-dialog-centered">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">{title}</h5>
              <button
                type="button"
                className="btn-close"
                onClick={onClose}
                aria-label="Cerrar"
              />
            </div>
            <div className="modal-body">
              {children}
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" onClick={onClose}>
                Cerrar
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}