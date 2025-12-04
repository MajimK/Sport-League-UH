const news = [
  {
    title: "🎾 Torneo Interfacultades de Tenis 2024",
    description: "La Facultad de Contabilidad lidera el cuadro de honor tras imponerse en dobles mixtos. Inscripciones abiertas hasta el 15 de diciembre.",
    image: "/static/images/tenis.jpg",
    link: "#"
  },
  {
    title: "♟️ Campeonato de Ajedrez Rápido",
    description: "Estudiantes de Contabilidad demuestran habilidades estratégicas en el torneo interdepartamental. Gran maestro internacional como invitado especial.",
    image: "/static/images/ajedrez.jpg",
    link: "#"
  },
  {
    title: "📊 Feria de Prácticas en Contabilidad",
    description: "Las Big Four visitan la facultad para reclutar talento. Talleres sobre nuevas normas IFRS y oportunidades de certificación CPA.",
    image: "/static/images/confin.jpg",
    link: "#"
  }
]

export default function NewsGrid() {
  return (
    <section className="news-block container">
      <h2>Noticias Universitarias</h2>
      <div className="news-grid">
        {news.map((item, index) => (
          <article key={index} className="news-card">
            <div className="news-img" style={{backgroundImage: `url(${item.image})`}}></div>
            <h3>{item.title}</h3>
            <p>{item.description}</p>
            <a href={item.link}>Ver detalles</a>
          </article>
        ))}
      </div>
    </section>
  )
}