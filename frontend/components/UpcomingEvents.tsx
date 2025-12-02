export default function UpcomingEvents() {
  const events = [
    {
      sport: "Baloncesto",
      date: "Hoy, 16:00h",
      teams: "Informática vs. Derecho",
      location: "Polideportivo Central"
    },
    {
      sport: "Fútbol",
      date: "Miércoles, 10:30h",
      teams: "FEU vs. Voluntarios",
      location: "Campo #3"
    }
  ]

  return (
    <section className="upcoming-events container">
      <h2>Próximos Eventos</h2>
      <div className="events-grid">
        {events.map((event, index) => (
          <div key={index} className="event-card">
            <span className="sport">{event.sport}</span>
            <span className="date">{event.date}</span>
            <p>{event.teams}</p>
            <span className="location">
              <i className="fas fa-map-marker-alt"></i> {event.location}
            </span>
          </div>
        ))}
      </div>
      <div className="text-center">
        <a href="#calendario" className="btn btn-blue-outline">Ver calendario completo</a>
      </div>
    </section>
  )
}