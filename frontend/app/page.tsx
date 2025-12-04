import HeroBanner from '@components/HeroBanner'
import NewsGrid from '@components/NewsGrid'
import LiveScores from '@components/LiveScores'
import UpcomingEvents from '@components/UpcomingEvents'

export default function Home() {
  return (
    <>
      <HeroBanner />
      <NewsGrid />
      <LiveScores />
      <UpcomingEvents />
    </>
  )
}