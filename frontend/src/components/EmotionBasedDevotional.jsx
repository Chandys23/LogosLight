import { useState } from 'react'
import { devotionalService } from '../utils/api'
import LoadingSpinner from './LoadingSpinner'

const PRESET_EMOTIONS = [
  '😔 Sad', '😰 Anxious', '😤 Angry', '😔 Lonely', '😩 Tired',
  '😞 Hopeless', '😕 Confused', '😠 Frustrated', '😢 Grieving', '🤔 Doubtful'
]

export default function EmotionBasedDevotional() {
  const [emotion, setEmotion] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async () => {
    const trimmed = emotion.trim()
    if (!trimmed) return
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const r = await devotionalService.getDevotional(trimmed)
      setResult(r.data)
    } catch (e) {
      setError(e.response?.data?.detail || 'Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className="max-w-3xl mx-auto py-8 space-y-6">
      <div className="text-center mb-10">
        <h2 className="text-3xl font-bold bg-gradient-to-r from-purple-300 to-blue-300 bg-clip-text text-transparent mb-2">
          How Are You Feeling?
        </h2>
        <p className="text-purple-300/60">
          Share your heart — God's Word meets you where you are.
        </p>
      </div>

      {/* Preset buttons */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-2 mb-6">
        {PRESET_EMOTIONS.map((e) => {
          const just_name = e.split(' ')[1]
          return (
            <button
              key={e}
              onClick={() => setEmotion(just_name)}
              className={`py-3 rounded-lg font-medium text-sm transition-all ${
                emotion === just_name
                  ? 'bg-amber-500/50 text-white border-2 border-amber-400'
                  : 'bg-slate-700/40 text-purple-200 hover:bg-slate-700/60 border border-purple-500/30'
              }`}
            >
              {e}
            </button>
          )
        })}
      </div>

      {/* Input form */}
      <div className="glass-card p-8 border-purple-500/30">
        <textarea
          value={emotion}
          onChange={(e) => setEmotion(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Describe what you're feeling...&#10;e.g. 'Struggling with a decision' · 'Feeling distant from God' · 'My heart is heavy'"
          rows={4}
          className="w-full bg-slate-700/50 border border-purple-500/30 rounded-lg px-4 py-3 text-gray-100 placeholder-purple-300/50 focus:outline-none focus:border-purple-400 focus:ring-1 focus:ring-purple-400/50 resize-none leading-relaxed"
        />

        <button
          onClick={handleSubmit}
          disabled={loading || !emotion.trim()}
          className="mt-6 w-full bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-500 hover:to-purple-600 disabled:opacity-40 text-white font-semibold py-3 rounded-lg transition-all"
        >
          {loading ? '🙏 Seeking Scripture...' : '🙏 Get Devotional'}
        </button>
      </div>

      {/* Error */}
      {error && (
        <div className="glass-card p-6 border-red-500/30 bg-red-500/10">
          <p className="text-red-300">{error}</p>
        </div>
      )}

      {/* Loading */}
      {loading && <LoadingSpinner message="Seeking God's comfort..." />}

      {/* Result */}
      {result && !loading && (
        <div className="space-y-6 animate-fadeIn">
          {/* Verses */}
          {result.verses && result.verses.length > 0 && (
            <div className="glass-card p-8 border-purple-500/30">
              <h3 className="text-amber-300 font-semibold mb-6 flex items-center gap-2">
                <span>📖</span> Verses for Your Heart
              </h3>
              <div className="space-y-4">
                {result.verses.map((v, i) => (
                  <div key={i} className="bg-slate-700/40 border-l-4 border-amber-400 rounded-lg p-5">
                    <p className="text-amber-300/80 text-sm font-semibold">{v.reference}</p>
                    <p className="text-gray-200 mt-3 italic">"{v.text}"</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Prayer */}
          {result.prayer && (
            <div className="glass-card p-8 bg-purple-500/10 border-purple-500/30">
              <h3 className="text-purple-300 font-semibold mb-4 flex items-center gap-2">
                <span>🙏</span> Prayer for You
              </h3>
              <p className="text-purple-100/80 leading-relaxed italic">{result.prayer}</p>
            </div>
          )}

          {/* Encouragement */}
          {result.encouragement && (
            <div className="glass-card p-8 bg-emerald-500/10 border-emerald-500/30">
              <h3 className="text-emerald-300 font-semibold mb-4 flex items-center gap-2">
                <span>✨</span> Encouragement
              </h3>
              <p className="text-emerald-100/80 leading-relaxed">{result.encouragement}</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
