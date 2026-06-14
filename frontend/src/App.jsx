import { useState } from 'react'
import VerseOfDay from './components/VerseOfDay'
import EmotionBasedDevotional from './components/EmotionBasedDevotional'
import AIDeepStudyGuide from './components/AIDeepStudyGuide'
import BibleReader from './components/BibleReader'

export default function App() {
  const [page, setPage] = useState('home')

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="border-b border-purple-700/30 bg-slate-900/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-8">
          <div className="flex items-center justify-between mb-6">
            <button
              onClick={() => setPage('home')}
              className="hover:opacity-80 transition-opacity"
            >
              <h1 className="text-4xl font-bold bg-gradient-to-r from-amber-300 via-purple-300 to-blue-300 bg-clip-text text-transparent">
                ✨ LogosLight
              </h1>
              <p className="text-purple-300/60 text-xs mt-1">Sacred Scripture + AI Wisdom</p>
            </button>
          </div>

          {/* Navigation Tabs */}
          <div className="flex gap-1 flex-wrap">
            {[
              { id: 'home', label: '📖 Verse of Day', icon: '✨' },
              { id: 'emotion', label: '💝 Emotional Devotional', icon: '🙏' },
              { id: 'study', label: '📚 Deep Study', icon: '🔍' },
              { id: 'bible', label: '✝️ KJV Bible', icon: '📕' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setPage(tab.id)}
                className={`px-4 py-3 font-medium text-sm transition-all duration-200 border-b-2 ${
                  page === tab.id
                    ? 'border-amber-400 text-amber-300'
                    : 'border-transparent text-purple-300/60 hover:text-purple-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 py-12">
        <div className="animate-fadeIn">
          {page === 'home' && <VerseOfDay />}
          {page === 'emotion' && <EmotionBasedDevotional />}
          {page === 'study' && <AIDeepStudyGuide />}
          {page === 'bible' && <BibleReader />}
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-purple-700/30 bg-slate-900/50 backdrop-blur-sm mt-12">
        <div className="max-w-6xl mx-auto px-4 py-8 text-center text-purple-300/50 text-sm space-y-2">
          <p>LogosLight • A free Christian devotional app — KJV Scripture + Claude AI</p>
          <p>"Your word is a lamp to my feet and a light to my path." — Psalm 119:105</p>
        </div>
      </footer>
    </div>
  )
}
