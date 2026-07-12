import { useEffect, useState } from 'react'

import { AuthForm } from './components/AuthForm'
import { getCurrentUser, loginUser, registerUser } from './lib/api'

interface UserProfile {
  id: number
  name: string
  email: string
}

function App() {
  const [mode, setMode] = useState<'login' | 'register'>('login')
  const [token, setToken] = useState<string | null>(localStorage.getItem('bluephish_token'))
  const [user, setUser] = useState<UserProfile | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadUser = async () => {
      if (!token) return
      try {
        const profile = await getCurrentUser(token)
        setUser(profile)
      } catch {
        localStorage.removeItem('bluephish_token')
        setToken(null)
      }
    }

    void loadUser()
  }, [token])

  const handleSubmit = async (payload: { name?: string; email: string; password: string }) => {
    setError(null)
    try {
      if (mode === 'register') {
        const result = await registerUser({
          name: payload.name || 'User',
          email: payload.email,
          password: payload.password,
        })
        localStorage.setItem('bluephish_token', result.access_token)
        setToken(result.access_token)
        setUser(result.user)
        return
      }

      const result = await loginUser({ email: payload.email, password: payload.password })
      localStorage.setItem('bluephish_token', result.access_token)
      setToken(result.access_token)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ha ocurrido un error')
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('bluephish_token')
    setToken(null)
    setUser(null)
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <main className="mx-auto flex max-w-6xl flex-col gap-8 px-6 py-16">
        <section className="rounded-2xl border border-slate-800 bg-slate-900/80 p-8 shadow-2xl shadow-cyan-950/40">
          <p className="text-sm uppercase tracking-[0.3em] text-cyan-400">BluePHish</p>
          <h1 className="mt-4 text-4xl font-semibold">Phishing Email Analyzer AI</h1>
          <p className="mt-4 max-w-2xl text-lg text-slate-400">
            Plataforma educativa para analizar correos sospechosos con reglas defensivas y explicaciones guiadas.
          </p>
        </section>

        {!token || !user ? (
          <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
            <section className="rounded-2xl border border-slate-800 bg-slate-900/80 p-8">
              <h2 className="text-2xl font-semibold text-white">Primeros pasos</h2>
              <ul className="mt-4 space-y-3 text-sm text-slate-400">
                <li>• Registra una cuenta para guardar tu historial.</li>
                <li>• Pega un correo sospechoso para analizar encabezados y URLs.</li>
                <li>• Recibe una puntuación de riesgo y recomendaciones guiadas.</li>
              </ul>
            </section>
            <AuthForm mode={mode} onSubmit={handleSubmit} error={error} />
          </div>
        ) : (
          <section className="rounded-2xl border border-slate-800 bg-slate-900/80 p-8">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <p className="text-sm uppercase tracking-[0.3em] text-cyan-400">Panel activo</p>
                <h2 className="mt-2 text-2xl font-semibold text-white">Bienvenido, {user.name}</h2>
                <p className="mt-1 text-slate-400">{user.email}</p>
              </div>
              <button
                onClick={handleLogout}
                className="rounded-lg border border-slate-700 px-4 py-2 text-sm text-slate-200 transition hover:border-cyan-500"
              >
                Cerrar sesión
              </button>
            </div>

            <div className="mt-8 grid gap-4 md:grid-cols-3">
              {[
                { label: 'Correos analizados', value: '0' },
                { label: 'Riesgo promedio', value: '—' },
                { label: 'Alertas recientes', value: '0' },
              ].map((item) => (
                <div key={item.label} className="rounded-xl border border-slate-800 bg-slate-950 p-5">
                  <p className="text-sm text-slate-400">{item.label}</p>
                  <p className="mt-2 text-3xl font-semibold text-white">{item.value}</p>
                </div>
              ))}
            </div>
          </section>
        )}

        <div className="flex gap-3 text-sm text-slate-400">
          <button onClick={() => setMode('login')} className={`rounded-full px-3 py-1 ${mode === 'login' ? 'bg-cyan-500 text-slate-950' : 'bg-slate-900'}`}>
            Iniciar sesión
          </button>
          <button onClick={() => setMode('register')} className={`rounded-full px-3 py-1 ${mode === 'register' ? 'bg-cyan-500 text-slate-950' : 'bg-slate-900'}`}>
            Registrarme
          </button>
        </div>
      </main>
    </div>
  )
}

export default App
