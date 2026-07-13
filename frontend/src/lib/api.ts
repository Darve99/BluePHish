const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers || {}),
    },
  })

  if (!response.ok) {
    const payload = await response.json().catch(() => ({}))
    throw new Error(payload.detail || 'Request failed')
  }

  return response.json() as Promise<T>
}

export async function registerUser(payload: { name: string; email: string; password: string }) {
  return request<{ user: { id: number; name: string; email: string }; access_token: string }>('/auth/register', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function loginUser(payload: { email: string; password: string }) {
  return request<{ access_token: string; token_type: string }>('/auth/login', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function getCurrentUser(token: string) {
  return request<{ id: number; name: string; email: string }>('/auth/me', {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
}

export async function analyzeEmail(token: string, rawEmail: string, file?: File | null) {
  if (file) {
    const formData = new FormData()
    formData.append('file', file)
    const response = await fetch(`${API_BASE_URL}/analysis/upload`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    })

    if (!response.ok) {
      const payload = await response.json().catch(() => ({}))
      throw new Error(payload.detail || 'No se pudo analizar el archivo')
    }

    return response.json() as Promise<{
      subject: string
      from: string
      to: string
      urls: string[]
      score: number
      risk_level: string
      summary: string
      indicators: Array<{ detail: string }>
    }>
  }

  return request<{
    subject: string
    from: string
    to: string
    urls: string[]
    score: number
    risk_level: string
    summary: string
    indicators: Array<{ detail: string }>
  }>('/analysis', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ raw_email: rawEmail }),
  })
}

export async function getHistory(token: string) {
  return request<Array<{
    id: number
    created_at: string
    subject: string
    score: number
    risk_level: string
    summary: string
  }>>('/history', {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
}

export async function downloadReport(token: string, rawEmail: string) {
  const response = await fetch(`${import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'}/report`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ raw_email: rawEmail }),
  })

  if (!response.ok) {
    throw new Error('No se pudo generar el reporte')
  }

  const blob = await response.blob()
  const url = window.URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = 'bluephish-report.pdf'
  link.click()
  window.URL.revokeObjectURL(url)
}
