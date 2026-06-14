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
      .catch(() => setError('Could not load verse. Please try refreshing.'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <LoadingSpinner message="Loading today's verse..." />

  if (error) return (
    <div className="bg-red-500/20 border border-red-500/40 text-red-300 rounded-xl p-6 text-center my-8">
      <p>{error}</p>
      <button onClick={() => window.location.reload()} className="mt-4 px-4 py-2 bg-red-500/30 hover:bg-red-500/50 rounded-lg text-sm">
        Refresh
      </button>
    </div>
  )

  return (
    <div className="bg-gradient-to-br from-purple-900/40 via-slate-800/40 to-purple-900/40 border border-purple-500/30 text-white rounded-2xl shadow-2xl p-10 md:p-14 my-8 text-center backdrop-blur-md animate-fadeIn">
      <p className="text-xs tracking-widest uppercase text-amber-300/80 font-semibold mb-8">
        ✦ Verse of the Day ✦
      </p>

      <blockquote className="text-xl md:text-3xl leading-relaxed italic mb-8 text-gray-100 font-serif">
        "{verse.text}"
      </blockquote>

      <p className="font-semibold text-amber-400 text-lg mb-12">
        — {verse.reference}
      </p>

      <div className="grid md:grid-cols-2 gap-6 text-left">
        <div className="bg-slate-700/30 backdrop-blur rounded-xl p-6 border border-purple-500/20">
          <p className="font-semibold text-purple-300 mb-3 text-sm uppercase tracking-wide">
            💭 Reflection
          </p>
          <p className="text-sm text-purple-100/80 leading-relaxed">{verse.reflection}</p>
        </div>
        <div className="bg-amber-900/20 backdrop-blur rounded-xl p-6 border border-amber-500/20">
          <p className="font-semibold text-amber-300 mb-3 text-sm uppercase tracking-wide">
            ⚡ Apply Today
          </p>
          <p className="text-sm text-amber-100/80 leading-relaxed">{verse.apply_today}</p>
        </div>
      </div>

      <button
        onClick={() => window.location.reload()}
        className="mt-10 px-6 py-3 bg-gradient-to-r from-amber-500/50 to-amber-600/50 hover:from-amber-500 hover:to-amber-600 rounded-lg font-semibold text-white transition-all duration-200"
      >
        🔄 Get Another Verse
      </button>
    </div>
  )
}
