import { useState } from 'react'
import VerseOfDay from './components/VerseOfDay'
import EmotionBasedDevotional from './components/EmotionBasedDevotional'
import AIDeepStudyGuide from './components/AIDeepStudyGuide'

const PAGES = {
  home:    'Home',
  emotion: 'Emotion-Based Devotional',
  study:   'AI Deep Study Guide',
}

export default function App() {
  const [page, setPage] = useState('home')

  return (
    <div className="min-h-screen bg-gradient-to-br from-spirit-cream via-white to-spirit-cream">

      {/* ── Navigation ── */}
      <nav className="bg-faith-blue shadow-lg sticky top-0 z-50">
        <div className="max-w-5xl mx-auto px-4 py-4 flex flex-col sm:flex-row justify-between items-center gap-3">
          <button
            onClick={() => setPage('home')}
            className="text-2xl font-bold text-divine-gold hover:opacity-90 transition"
          >
            🙏 LogosLight
          </button>

          <div className="flex gap-1 flex-wrap justify-center">
            {Object.entries(PAGES).map(([id, label]) => (
              <button
                key={id}
                onClick={() => setPage(id)}
                className={`px-4 py-2 rounded-lg font-medium text-sm transition-all ${
                  page === id
                    ? 'bg-divine-gold text-faith-blue shadow-sm'
                    : 'text-spirit-cream hover:text-divine-gold hover:bg-white/10'
                }`}
              >
                {label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* ── Content ── */}
      <main className="max-w-5xl mx-auto px-4 py-8">

        {page === 'home' && (
          <>
            <div className="text-center py-6">
              <h1 className="text-4xl md:text-5xl font-bold text-faith-blue mb-3">
                Welcome to LogosLight
              </h1>
              <p className="text-gray-500 text-lg">
                God's Word for every moment of your day
              </p>
            </div>

            <VerseOfDay />

            <div className="grid md:grid-cols-2 gap-6 mt-6">
              <button
                onClick={() => setPage('emotion')}
                className="text-left bg-white rounded-2xl shadow-md p-7 hover:shadow-xl transition-all border-t-4 border-divine-gold group"
              >
                <div className="text-3xl mb-3">💬</div>
                <h3 className="text-xl font-bold text-faith-blue mb-2 group-hover:text-divine-gold transition-colors">
                  Emotion-Based Devotional
                </h3>
                <p className="text-gray-500 text-sm leading-relaxed">
                  Share how you're feeling — get scripture, a personal prayer, and encouragement tailored to your heart.
                </p>
              </button>

              <button
                onClick={() => setPage('study')}
                className="text-left bg-white rounded-2xl shadow-md p-7 hover:shadow-xl transition-all border-t-4 border-faith-blue group"
              >
                <div className="text-3xl mb-3">📖</div>
                <h3 className="text-xl font-bold text-faith-blue mb-2 group-hover:text-[#2a5298] transition-colors">
                  AI Deep Study Guide
                </h3>
                <p className="text-gray-500 text-sm leading-relaxed">
                  Prepare sermons, explore Biblical topics, plan worship, or dive deep into any theological question.
                </p>
              </button>
            </div>
          </>
        )}

        {page === 'emotion' && <EmotionBasedDevotional />}
        {page === 'study'   && <AIDeepStudyGuide />}

      </main>

      {/* ── Footer ── */}
      <footer className="text-center py-8 text-gray-400 text-sm">
        <p>LogosLight · Built on the KJV (Public Domain) · Powered by Claude Haiku</p>
      </footer>
    </div>
  )
}
