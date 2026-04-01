const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export async function apiFetch(endpoint: string, options: RequestInit = {}) {
  const url = `${API_BASE}${endpoint}`
  const token = localStorage.getItem('token')
  
  const defaultHeaders = {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` })
  }

  const headers = {
    ...defaultHeaders,
    ... (options.headers as Record<string, string>)
  } as HeadersInit

  const config: RequestInit = {
    ...options,
    headers
  }

  const response = await fetch(url, config)
  
  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`)
  }
  
  return response.json()
}

