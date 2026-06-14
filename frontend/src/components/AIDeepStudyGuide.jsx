import { useState } from 'react'
import { studyService } from '../utils/api'
import LoadingSpinner from './LoadingSpinner'

const STUDY_SUGGESTIONS = [
  '💫 Faith', '🙏 Prayer', '❤️ Love', '💎 Grace', '🕊️ Forgiveness',
  '✝️ Salvation', '🧠 Wisdom', '💪 Strength', '✨ Holy Spirit', '🎵 Worship',
]

export default function AIDeepStudyGuide() {
  const [topic, setTopic] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSearch = async () => {
    const trimmed = topic.trim()
    if (!trimmed) return
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const r = await studyService.getStudyGuide(trimmed)
      setResult(r.data)
    } catch (e) {
      setError(e.response?.data?.detail || 'Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto py-8 space-y-6">
      <div className="text-center mb-10">
        <h2 className="text-3xl font-bold bg-gradient-to-r from-blue-300 to-purple-300 bg-clip-text text-transparent mb-2">
          Deep Scripture Study
        </h2>
        <p className="text-blue-300/60">
          Sermon prep · Topical deep-dive · Theological questions · Worship planning
        </p>
      </div>

      {/* Quick topic chips */}
      <div className="flex flex-wrap gap-2 mb-6">
        {STUDY_SUGGESTIONS.map((s) => (
          <button
            key={s}
            onClick={() => {
              const clean = s.split(' ').slice(1).join(' ')
              setTopic(clean)
            }}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
              topic.split(' ').join(' ') === s.split(' ').slice(1).join(' ')
                ? 'bg-blue-500/60 text-white border-2 border-blue-400'
                : 'bg-slate-700/40 text-blue-200 border border-blue-500/30 hover:bg-slate-700/60'
            }`}
          >
            {s}
          </button>
        ))}
      </div>

      {/* Search form */}
      <div className="glass-card p-8 border-blue-500/30">
        <input
          type="text"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          placeholder="Enter any topic, verse, character, or theological question…"
          className="w-full bg-slate-700/50 border border-blue-500/30 rounded-lg px-4 py-3 text-gray-100 placeholder-blue-300/50 focus:outline-none focus:border-blue-400 focus:ring-1 focus:ring-blue-400/50 mb-6"
        />

        <button
          onClick={handleSearch}
          disabled={loading || !topic.trim()}
          className="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-500 hover:to-blue-600 disabled:opacity-40 text-white font-semibold py-3 rounded-lg transition-all"
        >
          {loading ? '📖 Studying Scripture...' : '📖 Generate Study Guide'}
        </button>
      </div>

      {/* Error */}
      {error && (
        <div className="glass-card p-6 border-red-500/30 bg-red-500/10">
          <p className="text-red-300">{error}</p>
        </div>
      )}

      {/* Loading */}
      {loading && <LoadingSpinner message="Preparing your study guide..." />}

      {/* Result */}
      {result && !loading && (
        <div className="space-y-6 animate-fadeIn">
          {/* Key Verses */}
          {result.verses && result.verses.length > 0 && (
            <div className="glass-card p-8 border-blue-500/30">
              <h3 className="text-blue-300 font-semibold mb-6 flex items-center gap-2">
                <span>📖</span> Key Verses
              </h3>
              <div className="space-y-4">
                {result.verses.map((v, i) => (
                  <div key={i} className="bg-slate-700/40 border-l-4 border-blue-400 rounded-lg p-5">
                    <p className="text-blue-300/80 text-sm font-semibold">{v.reference}</p>
                    <p className="text-gray-200 mt-3 italic">"{v.text}"</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Study Guide */}
          {result.study_guide && (
            <div className="glass-card p-8 bg-blue-500/10 border-blue-500/30">
              <h3 className="text-blue-300 font-semibold mb-6 flex items-center gap-2">
                <span>🎓</span> Study Guide
              </h3>
              <div className="text-gray-200 leading-relaxed whitespace-pre-line text-sm">
                {result.study_guide}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
