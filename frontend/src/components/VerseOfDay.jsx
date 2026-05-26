import { useEffect, useState } from 'react'
import { verseService } from '../utils/api'
import LoadingSpinner from './LoadingSpinner'

export default function VerseOfDay() {
  const [verse, setVerse] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    verseService.getVerseOfDay()
      .then((r) => setVerse(r.data))
      .catch(() => setError('Could not load today\'s verse. Please refresh.'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <LoadingSpinner message="Loading today's verse..." />

  if (error) return (
    <div className="bg-red-50 border border-red-200 text-red-700 rounded-xl p-6 text-center my-8">
      {error}
    </div>
  )

  return (
    <div className="bg-gradient-to-br from-faith-blue to-[#2a5298] text-white rounded-2xl shadow-2xl p-8 md:p-12 my-8 text-center">
      <p className="text-xs tracking-[0.2em] uppercase text-divine-gold font-semibold mb-6">
        ✦ Verse of the Day ✦
      </p>

      <blockquote className="font-scripture text-xl md:text-3xl leading-relaxed italic mb-6 text-spirit-cream">
        "{verse.text}"
      </blockquote>

      <p className="font-semibold text-divine-gold text-lg mb-8">
        — {verse.reference}
      </p>

      <div className="grid md:grid-cols-2 gap-4 text-left">
        <div className="bg-white/10 backdrop-blur rounded-xl p-5">
          <p className="font-semibold text-divine-gold mb-2 text-sm uppercase tracking-wide">
            Reflection
          </p>
          <p className="text-sm text-spirit-cream/90 leading-relaxed">{verse.reflection}</p>
        </div>
        <div className="bg-white/10 backdrop-blur rounded-xl p-5">
          <p className="font-semibold text-divine-gold mb-2 text-sm uppercase tracking-wide">
            Apply Today
          </p>
          <p className="text-sm text-spirit-cream/90 leading-relaxed">{verse.apply_today}</p>
        </div>
      </div>
    </div>
  )
}
