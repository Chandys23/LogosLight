import { useState } from 'react'
import { devotionalService } from '../utils/api'
import LoadingSpinner from './LoadingSpinner'

const PRESET_EMOTIONS = [
  'Anxious', 'Sad', 'Lost', 'Grateful',
  'Seeking', 'Joyful', 'Overwhelmed', 'Lonely', 'Hopeful',
]

export default function EmotionBasedDevotional() {
  const [emotion, setEmotion] = useState('')
  const [result, setResult]   = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState(null)

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
    <div className="max-w-3xl mx-auto py-8">
      <h2 className="text-3xl font-bold text-faith-blue text-center mb-2">
        How Are You Feeling?
      </h2>
      <p className="text-center text-gray-500 mb-8">
        Share your heart — God's Word meets you where you are.
      </p>

      {/* Preset buttons */}
      <div className="grid grid-cols-3 md:grid-cols-5 gap-2 mb-5">
        {PRESET_EMOTIONS.map((e) => (
          <button
            key={e}
            onClick={() => setEmotion(e)}
            className={`py-2.5 rounded-lg font-medium text-sm transition-all ${
              emotion === e
                ? 'bg-divine-gold text-white shadow-md scale-105'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {e}
          </button>
        ))}
      </div>

      {/* Open text input */}
      <textarea
        value={emotion}
        onChange={(e) => setEmotion(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Or describe how you're feeling in your own words…&#10;e.g. 'Struggling with a big decision' · 'Feeling distant from God' · 'My heart is heavy today'"
        rows={3}
        className="w-full border border-gray-300 rounded-xl p-4 text-gray-700 focus:outline-none focus:ring-2 focus:ring-faith-blue focus:border-transparent mb-4 resize-none leading-relaxed"
      />

      <button
        onClick={handleSubmit}
        disabled={loading || !emotion.trim()}
        className="w-full bg-faith-blue text-white py-4 rounded-xl font-semibold text-lg hover:bg-[#2a5298] disabled:opacity-40 transition-all shadow-md"
      >
        {loading ? 'Finding scripture for you…' : 'Get Devotional'}
      </button>

      {error && (
        <div className="mt-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl">
          {error}
        </div>
      )}

      {loading && <LoadingSpinner message="Searching scripture…" />}

      {result && !loading && (
        <div className="mt-10 space-y-6 animate-fade-in">
          {/* Verses */}
          <div>
            <h3 className="text-lg font-bold text-faith-blue mb-4 flex items-center gap-2">
              <span>📖</span> Relevant Verses
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

          {/* Prayer */}
          <div className="bg-green-50 border-l-4 border-life-green rounded-xl p-6">
            <h3 className="font-bold text-faith-blue mb-3 flex items-center gap-2">
              <span>🙏</span> Prayer
            </h3>
            <p className="text-gray-700 leading-relaxed whitespace-pre-line">{result.prayer}</p>
          </div>

          {/* Encouragement */}
          <div className="bg-purple-50 border-l-4 border-spirit-purple rounded-xl p-6">
            <h3 className="font-bold text-faith-blue mb-3 flex items-center gap-2">
              <span>✨</span> Encouragement
            </h3>
            <p className="text-gray-700 leading-relaxed whitespace-pre-line">{result.encouragement}</p>
          </div>

          {/* Full Claude response if there's more */}
          {result.full_response &&
            result.full_response.length > result.prayer.length + result.encouragement.length + 100 && (
            <details className="bg-gray-50 border border-gray-200 rounded-xl p-4">
              <summary className="cursor-pointer text-faith-blue font-medium text-sm">
                View full response
              </summary>
              <div className="mt-3 text-gray-700 leading-relaxed whitespace-pre-line text-sm">
                {result.full_response}
              </div>
            </details>
          )}
        </div>
      )}
    </div>
  )
}
