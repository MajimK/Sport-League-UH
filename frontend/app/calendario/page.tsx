'use client';

import { useState } from 'react';
import {
  startOfMonth,
  startOfWeek,
  addMonths,
  subMonths,
  isSameMonth,
  isSameDay,
  format,
} from 'date-fns';
import { es } from 'date-fns/locale';

// Eventos con descripción
const EVENTS = [
  {
    id: 1,
    title: "Torneo de Tenis",
    date: "2026-01-10",
    description: "Final del torneo interfacultades de tenis. Participan las 8 mejores parejas."
  },
  {
    id: 2,
    title: "Entrenamiento Baloncesto",
    date: "2026-01-15",
    description: "Sesión técnica y física para el equipo Caribe. Obligatorio para todos los jugadores."
  },
  {
    id: 3,
    title: "Final de Fútbol",
    date: "2026-01-22",
    description: "¡Gran final! Contabilidad vs Matemática. Estadio universitario, 4:00 PM."
  },
  {
    id: 4,
    title: "Clínica de Ajedrez",
    date: "2026-01-28",
    description: "Clínica abierta para principiantes y avanzados. Impartida por el Maestro Nacional."
  },
  {
    id: 5,
    title: "Reunión Técnica",
    date: "2026-02-03",
    description: "Coordinación de árbitros y logística para el próximo torneo."
  },
];

const eventsByDate = new Map(EVENTS.map(event => [event.date, event]));

export default function CalendarioPage() {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [hoverEvent, setHoverEvent] = useState<{ event: typeof EVENTS[0]; x: number; y: number } | null>(null);

  const goToPreviousMonth = () => setCurrentDate(subMonths(currentDate, 1));
  const goToNextMonth = () => setCurrentDate(addMonths(currentDate, 1));

  const monthStart = startOfMonth(currentDate);
  const startDate = startOfWeek(monthStart, { locale: es });

  const days = [];
  let day = new Date(startDate);

  for (let i = 0; i < 42; i++) {
    const isCurrentMonth = isSameMonth(day, monthStart);
    const isToday = isSameDay(day, new Date());
    const dayKey = format(day, 'yyyy-MM-dd');
    const event = eventsByDate.get(dayKey);

    days.push(
      <div
        key={i}
        className={`p-3 text-center border position-relative ${
          !isCurrentMonth
            ? 'text-muted bg-light'
            : isToday
            ? 'fw-bold text-primary bg-white'
            : 'bg-white'
        }`}
        style={{ minHeight: '70px', cursor: event ? 'pointer' : 'default' }}
        onMouseEnter={(e) => {
          if (event) {
            setHoverEvent({
              event,
              x: e.clientX,
              y: e.clientY,
            });
          }
        }}
        onMouseLeave={() => {
          setHoverEvent(null);
        }}
      >
        <div>{format(day, 'd')}</div>
        {event && isCurrentMonth && (
          <span
            className="position-absolute"
            style={{
              bottom: '8px',
              left: '50%',
              transform: 'translateX(-50%)',
              width: '6px',
              height: '6px',
              backgroundColor: '#dc3545',
              borderRadius: '50%',
            }}
          />
        )}
      </div>
    );

    day.setDate(day.getDate() + 1);
  }

  const dayNames = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];

  return (
    <>
      <div className="text-center py-4 bg-white border-bottom">
        <h1 className="mb-0">Calendario Deportivo</h1>
        <p className="text-muted">Universidad de La Habana</p>
      </div>

      <div className="d-flex justify-content-center w-100 px-3 py-4">
        <div className="w-100" style={{ maxWidth: '800px' }}>
          <div className="d-flex justify-content-between align-items-center mb-3">
            <button className="btn btn-outline-secondary" onClick={goToPreviousMonth}>
              ‹ Mes anterior
            </button>
            <h2 className="mb-0 text-dark">
              {format(currentDate, 'MMMM yyyy', { locale: es })}
            </h2>
            <button className="btn btn-outline-secondary" onClick={goToNextMonth}>
              Mes siguiente ›
            </button>
          </div>

          <div className="d-grid grid-column-7 text-center fw-bold mb-0 border">
            {dayNames.map((name, i) => (
              <div key={i} className="p-2 bg-light border-bottom-0">
                {name}
              </div>
            ))}
          </div>

          <div className="d-grid grid-column-7 border">{days}</div>
        </div>
      </div>

      {/* Tooltip personalizado: sigue al mouse */}
      {hoverEvent && (
        <div
          className="px-3 py-2"
          style={{
            position: 'fixed',
            top: hoverEvent.y + 10,
            left: hoverEvent.x + 10,
            backgroundColor: 'rgba(0, 0, 0, 0.9)',
            color: 'white',
            borderRadius: '6px',
            maxWidth: '300px',
            zIndex: 10000,
            pointerEvents: 'none', // evita interferir con el hover
            fontSize: '14px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.3)',
          }}
        >
          <div className="fw-bold">{hoverEvent.event.title}</div>
          <div className="mt-1 small">{hoverEvent.event.description}</div>
        </div>
      )}

      <style jsx>{`
        .grid-column-7 {
          grid-template-columns: repeat(7, 1fr);
        }
        .border {
          border: 1px solid #dee2e6;
        }
        .border-bottom-0 {
          border-bottom: none;
        }
      `}</style>
    </>
  );
}