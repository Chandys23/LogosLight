import { useState, useEffect } from 'react'
import axios from 'axios'
import LoadingSpinner from './LoadingSpinner'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function BibleReader() {
  const [books, setBooks] = useState([])
  const [selectedBook, setSelectedBook] = useState('')
  const [chapters, setChapters] = useState([])
  const [selectedChapter, setSelectedChapter] = useState(null)
  const [verses, setVerses] = useState([])
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [mode, setMode] = useState('browse')
  const [error, setError] = useState(null)

  // Fetch all books on mount
  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const res = await axios.get(`${API_BASE}/api/bible/books`)
        setBooks(res.data.books)
        if (res.data.books.length > 0) {
          setSelectedBook(res.data.books[0].book)
        }
      } catch (err) {
        setError('Failed to load Bible books')
      }
    }
    fetchBooks()
  }, [])

  // Fetch chapters when book is selected
  useEffect(() => {
    if (selectedBook) {
      const fetchChapters = async () => {
        try {
          const res = await axios.get(`${API_BASE}/api/bible/${selectedBook}/chapters`)
          setChapters(res.data.chapters)
          setSelectedChapter(1)
          setVerses([])
        } catch (err) {
          setError(`Failed to load chapters for ${selectedBook}`)
        }
      }
      fetchChapters()
    }
  }, [selectedBook])

  // Fetch verses when chapter is selected
  useEffect(() => {
    if (selectedBook && selectedChapter) {
      const fetchVerses = async () => {
        setLoading(true)
        try {
          const res = await axios.get(`${API_BASE}/api/bible/${selectedBook}/${selectedChapter}`)
          setVerses(res.data.verses)
          setError(null)
        } catch (err) {
          setError(`Failed to load chapter`)
        } finally {
          setLoading(false)
        }
      }
      fetchVerses()
    }
  }, [selectedBook, selectedChapter])

  // Handle search
  const handleSearch = async () => {
    if (searchQuery.trim().length < 2) return

    setLoading(true)
    setMode('search')
    try {
      const res = await axios.get(`${API_BASE}/api/bible/search`, {
        params: { q: searchQuery }
      })
      setSearchResults(res.data.verses)
      setError(null)
    } catch (err) {
      setError('Search failed or no results found')
      setSearchResults([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center mb-10">
        <h2 className="text-3xl font-bold bg-gradient-to-r from-blue-300 to-purple-300 bg-clip-text text-transparent mb-2">
          📖 KJV Bible Reader
        </h2>
        <p className="text-blue-300/60">Read the complete King James Version</p>
      </div>

      {/* Mode Tabs */}
      <div className="flex gap-2 border-b border-purple-700/30">
        <button
          onClick={() => setMode('browse')}
          className={`px-4 py-3 font-medium transition-all border-b-2 ${
            mode === 'browse'
              ? 'border-amber-400 text-amber-300'
              : 'border-transparent text-purple-300/60 hover:text-purple-300'
          }`}
        >
          📚 Browse
        </button>
        <button
          onClick={() => setMode('search')}
          className={`px-4 py-3 font-medium transition-all border-b-2 ${
            mode === 'search'
              ? 'border-amber-400 text-amber-300'
              : 'border-transparent text-purple-300/60 hover:text-purple-300'
          }`}
        >
          🔍 Search
        </button>
      </div>

      {error && (
        <div className="glass-card p-6 bg-red-500/10 border-red-500/30">
          <p className="text-red-300">{error}</p>
        </div>
      )}

      {/* BROWSE MODE */}
      {mode === 'browse' && (
        <div className="space-y-6">
          {/* Book Selector */}
          <div className="glass-card p-8 border-purple-500/30">
            <label className="block text-sm font-semibold text-purple-300 mb-4 uppercase tracking-wide">
              Select Book
            </label>
            <select
              value={selectedBook}
              onChange={(e) => setSelectedBook(e.target.value)}
              className="w-full bg-slate-700/50 border border-purple-500/30 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-purple-400"
            >
              {books.map((b) => (
                <option key={b.book} value={b.book}>
                  {b.book} ({b.verse_count} verses)
                </option>
              ))}
            </select>
          </div>

          {/* Chapter Selector */}
          {chapters.length > 0 && (
            <div className="glass-card p-8 border-purple-500/30">
              <label className="block text-sm font-semibold text-purple-300 mb-4 uppercase tracking-wide">
                Select Chapter
              </label>
              <div className="grid grid-cols-6 md:grid-cols-10 gap-2">
                {chapters.map((ch) => (
                  <button
                    key={ch}
                    onClick={() => setSelectedChapter(ch)}
                    className={`px-3 py-2 rounded font-medium transition-all ${
                      selectedChapter === ch
                        ? 'bg-amber-500/50 text-white border-2 border-amber-400'
                        : 'bg-slate-700/40 text-purple-200 hover:bg-slate-700/60 border border-purple-500/20'
                    }`}
                  >
                    {ch}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Verses Display */}
          {loading && <LoadingSpinner message="Loading chapter..." />}

          {verses.length > 0 && !loading && (
            <div className="glass-card p-8 border-purple-500/30">
              <div className="text-center mb-8 pb-6 border-b border-purple-500/20">
                <h3 className="text-3xl font-bold text-amber-300">
                  {selectedBook} {selectedChapter}
                </h3>
                <p className="text-purple-300/60 text-sm mt-2">{verses.length} verses</p>
              </div>
              <div className="space-y-6 max-h-96 overflow-y-auto pr-4">
                {verses.map((v) => (
                  <div key={v.verse} className="border-l-4 border-amber-400 pl-4">
                    <p className="text-amber-300/80 text-xs font-bold mb-2 uppercase tracking-wider">
                      Verse {v.verse}
                    </p>
                    <p className="text-gray-200 leading-relaxed italic text-sm">
                      "{v.text}"
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* SEARCH MODE */}
      {mode === 'search' && (
        <div className="space-y-6">
          <div className="glass-card p-8 border-blue-500/30">
            <label className="block text-sm font-semibold text-blue-300 mb-4 uppercase tracking-wide">
              Search Scripture
            </label>
            <div className="flex gap-3">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                placeholder="Search for words, topics, or verses..."
                className="flex-1 bg-slate-700/50 border border-blue-500/30 rounded-lg px-4 py-3 text-white placeholder-blue-300/50 focus:outline-none focus:border-blue-400"
              />
              <button
                onClick={handleSearch}
                disabled={loading || searchQuery.trim().length < 2}
                className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-500 hover:to-blue-600 disabled:opacity-40 text-white font-semibold px-6 py-3 rounded-lg transition-all whitespace-nowrap"
              >
                {loading ? '🔍' : '🔎 Search'}
              </button>
            </div>
          </div>

          {loading && <LoadingSpinner message="Searching Scripture..." />}

          {searchResults.length > 0 && !loading && (
            <div className="glass-card p-8 bg-blue-500/10 border-blue-500/30">
              <h3 className="text-xl font-bold text-blue-300 mb-6">
                Found {searchResults.length} verses
              </h3>
              <div className="space-y-5 max-h-96 overflow-y-auto pr-4">
                {searchResults.map((v, idx) => (
                  <div key={idx} className="border-l-4 border-blue-400 pl-4">
                    <p className="text-blue-300/80 text-xs font-bold mb-2 uppercase tracking-wider">
                      {v.reference}
                    </p>
                    <p className="text-gray-200 leading-relaxed italic text-sm">
                      "{v.text}"
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {!loading && searchResults.length === 0 && searchQuery.trim() && (
            <div className="glass-card p-8 text-center border-blue-500/30">
              <p className="text-purple-300/70">No verses found matching "{searchQuery}"</p>
              <p className="text-purple-300/50 text-sm mt-2">Try searching for different words or topics</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
