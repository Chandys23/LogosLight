import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' },
  timeout: 30000,
})

export const verseService = {
  getVerseOfDay: () => api.get('/api/verses/verse-of-day'),
}

export const devotionalService = {
  getDevotional: (emotion) =>
    api.post('/api/devotional/emotion', { emotion }),
}

export const studyService = {
  getStudyGuide: (topic) =>
    api.post('/api/ai-study/search', { topic }),
}

export default api
