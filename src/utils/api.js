// Centralized API fetch helper
// - In dev, Vite proxy handles '/api'
// - In Vercel full-stack, '/api' is routed to Python (main.py)
// - Allow override via VITE_API_BASE_URL when needed

const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api';

export function apiUrl(path) {
  if (!path.startsWith('/')) path = `/${path}`;
  return `${API_BASE}${path}`;
}

export async function apiFetch(path, options) {
  const url = apiUrl(path);
  return fetch(url, options);
}
