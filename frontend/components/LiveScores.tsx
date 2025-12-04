export default function LiveScores() {
  return (
    <section className="live-scores">
      <div className="ticker container">
        <span><i className="fas fa-tennis-ball"></i> Tenis: Contabilidad 3 - 2 Economía</span>
        <span><i className="fas fa-chess"></i> Ajedrez: F. Contabilidad vs Matemática (En juego)</span>
        <span><i className="fas fa-medal"></i> Medallero: 1.º Contabilidad | 2.º Matemática | 3.º Economía</span>
        <a href="#resultados" className="btn-ticker">Ver todos los resultados</a>
      </div>
    </section>
  )
}