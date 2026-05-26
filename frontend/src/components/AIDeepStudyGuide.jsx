import { useState } from 'react'
import { studyService } from '../utils/api'
import LoadingSpinner from './LoadingSpinner'

const STUDY_SUGGESTIONS = [
  'Faith', 'Prayer', 'Love', 'Grace', 'Forgiveness',
  'Salvation', 'Wisdom', 'Strength', 'The Holy Spirit', 'Worship',
]

export default function AIDeepStudyGuide() {
  const [topic, setTopic]     = useState('')
  const [result, setResult]   = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState(null)

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
    <div className="max-w-3xl mx-auto py-8">
      <h2 className="text-3xl font-bold text-faith-blue text-center mb-2">
        AI Deep Study Guide
      </h2>
      <p className="text-center text-gray-500 mb-8">
        Sermon prep · Scripture deep-dive · Worship planning · Theological questions
      </p>

      {/* Quick topic chips */}
      <div className="flex flex-wrap gap-2 mb-5">
        {STUDY_SUGGESTIONS.map((s) => (
          <button
            key={s}
            onClick={() => setTopic(s)}
            className={`px-4 py-2 rounded-full text-sm font-medium border transition-all ${
              topic === s
                ? 'bg-faith-blue text-white border-faith-blue shadow-md'
                : 'bg-white text-faith-blue border-faith-blue hover:bg-faith-blue hover:text-white'
            }`}
          >
            {s}
          </button>
        ))}
      </div>

      {/* Open text input */}
      <input
        type="text"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
        placeholder="Enter any topic, verse, character, or theological question…"
        className="w-full border border-gray-300 rounded-xl p-4 text-gray-700 focus:outline-none focus:ring-2 focus:ring-faith-blue focus:border-transparent mb-4"
      />

      <button
        onClick={handleSearch}
        disabled={loading || !topic.trim()}
        className="w-full bg-faith-blue text-white py-4 rounded-xl font-semibold text-lg hover:bg-[#2a5298] disabled:opacity-40 transition-all shadow-md"
      >
        {loading ? 'Studying scripture…' : 'Generate Study Guide'}
      </button>

      {error && (
        <div className="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl">
          {error}
        </div>
      )}

      {loading && <LoadingSpinner message="Preparing your study guide…" />}

      {result && !loading && (
        <div className="mt-10 space-y-6">
          {/* Key Verses */}
          <div>
            <h3 className="text-lg font-bold text-faith-blue mb-4 flex items-center gap-2">
              <span>📖</span> Key Verses
            </h3>
            {result.verses.map((v, i) => (
              <div
                key={i}
                className="bg-spirit-cream border-l-4 border-divine-gold rounded-xl p-5 mb-4"
              >
                <p className="font-semibold text-faith-blue mb-2">{v.reference}</p>
                <p className="font-scripture italic text-gray-800 leading-relaxed">"{v.text}"</p>
              </div>
            ))}
          </div>

          {/* Study Guide */}
          <div className="bg-blue-50 border-l-4 border-faith-blue rounded-xl p-6">
            <h3 className="font-bold text-faith-blue mb-4 flex items-center gap-2">
              <span>🎓</span> Study Guide
            </h3>
            <div className="text-gray-700 leading-relaxed whitespace-pre-line">
              {result.study_guide}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
