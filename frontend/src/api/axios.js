import axios from 'axios'

const api = axios.create({
  baseURL: window.ENV?.VITE_API_URL || import.meta.env.VITE_API_URL || 'http://localhost:5000/api/v1',
})

export default api
