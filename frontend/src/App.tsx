import { useEffect, useState } from 'react'
import { LogOut } from 'lucide-react'
import { AdminPanel } from './components/AdminPanel'
import { AuthForm } from './components/AuthForm'
import { EmailAnalysisForm } from './components/EmailAnalysisForm'
import { HistoryList } from './components/HistoryList'
import { RiskDistributionChart } from './components/RiskDistributionChart'
import { analyzeEmail, getCurrentUser, getHistory, loginUser, registerUser } from './lib/api'

interface UserProfile {
  id: number
  name: string
  email: string
}

function App() {
  const [mode, setMode] = useState<'login' | 'register'>('login')
  const [token, setToken] = useState<string | null>(localStorage.getItem('bluephish_token'))
  const [user, setUser] = useState<UserProfile | null>(null)
  const [isGuest, setIsGuest] = useState(false)
  const [theme, setTheme] = useState<'system' | 'light' | 'dark'>(() => {
    try {
      return (localStorage.getItem('bluephish_theme') as 'system' | 'light' | 'dark') || 'system'
    } catch {
      return 'system'
    }
  })
  const [error, setError] = useState<string | null>(null)
  const [analysisResult, setAnalysisResult] = useState<{
    subject?: string
    from?: string
    to?: string
    score?: number
    risk_level?: string
    summary?: string
    indicators?: Array<{ detail: string }>
    urls?: string[]
  } | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [history, setHistory] = useState<Array<{ id: number; created_at: string; subject: string; score: number; risk_level: string; summary: string }>>([])

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

  useEffect(() => {
    const loadHistory = async () => {
      if (!token) return
      try {
        const entries = await getHistory(token)
        setHistory(entries)
      } catch {
        setHistory([])
      }
    }

    void loadHistory()
  }, [token])

  // Apply theme preference
  useEffect(() => {
    const apply = (mode: 'system' | 'light' | 'dark') => {
      const root = document.documentElement
      if (mode === 'light') {
        root.classList.remove('dark')
      } else if (mode === 'dark') {
        root.classList.add('dark')
      } else {
        const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
        if (prefersDark) root.classList.add('dark')
        else root.classList.remove('dark')
      }
    }

    apply(theme)
    try {
      localStorage.setItem('bluephish_theme', theme)
    } catch {}

    if (theme === 'system' && window.matchMedia) {
      const mq = window.matchMedia('(prefers-color-scheme: dark)')
      const handler = () => apply('system')
      mq.addEventListener('change', handler)
      return () => mq.removeEventListener('change', handler)
    }
  }, [theme])

  const toggleTheme = () => {
    setTheme((t) => (t === 'system' ? 'light' : t === 'light' ? 'dark' : 'system'))
  }

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

  const handleGuestStart = () => {
    // Clear any token and mark guest mode
    localStorage.removeItem('bluephish_token')
    setToken(null)
    setUser(null)
    setIsGuest(true)
  }

  const handleAnalyze = async (rawEmail: string, file?: File | null, subject?: string, hasAttachment?: boolean) => {
    setIsAnalyzing(true)
    try {
      if (isGuest) {
        const result = await (await import('./lib/api')).analyzeGuest(rawEmail, file)
        // if subject provided, prefer it
        if (subject) result.subject = subject
        // apply attachment bump locally if provided
        if (hasAttachment) {
          result.score = Math.min(100, (result.score || 0) + 10)
          result.risk_level = result.score >= 70 ? 'high' : result.score >= 30 ? 'medium' : 'low'
        }
        setAnalysisResult(result)
        return
      }

      if (!token) return

      const result = await analyzeEmail(token, rawEmail, file, subject, hasAttachment)
      setAnalysisResult(result)
      const entries = await getHistory(token)
      setHistory(entries)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'No se pudo analizar el mensaje')
    } finally {
      setIsAnalyzing(false)
    }
  }

  return (
    <div className="relative min-h-screen bg-slate-50 text-slate-900">
      <div className="pointer-events-none absolute inset-x-0 top-0 h-80 bg-[radial-gradient(circle_at_top_left,_rgba(56,189,248,0.18),_transparent_24%),radial-gradient(circle_at_top_right,_rgba(52,211,153,0.14),_transparent_20%)] blur-3xl" />
      <main className="relative mx-auto max-w-7xl px-6 py-10 sm:px-8">
        <header className="relative overflow-hidden rounded-[2rem] border border-slate-200 bg-white shadow-[0_30px_60px_rgba(15,23,42,0.08)]">
          <div className="absolute -right-16 top-16 h-40 w-40 rounded-full bg-sky-100/90 blur-3xl"></div>
          <div className="absolute left-10 top-24 h-28 w-28 rounded-full bg-emerald-100/90 blur-3xl"></div>
          <div className="relative grid gap-8 lg:grid-cols-[1.2fr_0.9fr] p-10">
            <div className="absolute right-6 top-6 z-10 flex items-center gap-3">
              <button
                onClick={toggleTheme}
                title={`Tema: ${theme}`}
                className="rounded-full border border-slate-200 bg-slate-50 px-3 py-2 text-sm transition hover:bg-slate-100"
              >
                {theme === 'system' ? '🖥️' : theme === 'light' ? '🌞' : '🌙'}
              </button>
            </div>
            <div className="max-w-2xl">
              <p className="text-sm font-semibold uppercase tracking-[0.35em] text-slate-500">BluePHish</p>
              <h1 className="mt-4 text-5xl font-semibold tracking-tight text-slate-950 sm:text-6xl">
                Un lugar seguro para revisar correos y enlaces con calma.
              </h1>
              
              <div className="mt-8 flex flex-wrap gap-3">
                <span className="rounded-full bg-sky-100 px-4 py-2 text-sm font-medium text-sky-800">Fácil de usar</span>
                <span className="rounded-full bg-amber-100 px-4 py-2 text-sm font-medium text-amber-900">Seguro</span>
              </div>
            </div>
            <div className="rounded-[2rem] border border-slate-200 bg-slate-50 p-7 shadow-[0_25px_45px_rgba(15,23,42,0.08)]">
              <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Cómo ayuda</p>
              <h2 className="mt-3 text-3xl font-semibold text-slate-950">Revisa correos sin estrés</h2>
              <div className="mt-8 grid gap-4">
                <div className="rounded-[1.75rem] bg-white p-5 shadow-sm">
                  <p className="text-sm font-semibold text-slate-700">Analiza texto y archivos</p>
                  <p className="mt-2 text-sm leading-6 text-slate-600">Pega un correo o sube un archivo .eml y obtén un veredicto claro.</p>
                </div>
                <div className="rounded-[1.75rem] bg-white p-5 shadow-sm">
                  <p className="text-sm font-semibold text-slate-700">Señales que puedes entender</p>
                  <p className="mt-2 text-sm leading-6 text-slate-600">Recibe una lista de indicadores comunes y qué significan.</p>
                </div>
                <div className="rounded-[1.75rem] bg-white p-5 shadow-sm">
                  <p className="text-sm font-semibold text-slate-700">Historial accesible</p>
                  <p className="mt-2 text-sm leading-6 text-slate-600">Consulta tus análisis anteriores cuando quieras.</p>
                </div>
              </div>
            </div>
          </div>
        </header>

        {!token && !isGuest ? (
          <div className="grid gap-8 lg:grid-cols-[1.2fr_0.8fr]">
            <section className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-[0_30px_60px_rgba(15,23,42,0.08)]">
              <h2 className="text-3xl font-semibold text-slate-950">Cuando algo no te cuadra</h2>
              <p className="mt-4 text-slate-600 leading-7">
                BluePHish te ayuda a identificar si un correo parece sospechoso. Empieza con tu primer análisis y recibe una guía amigable.
              </p>
              <div className="mt-8 space-y-4">
                <div className="rounded-[1.75rem] border border-slate-200 bg-sky-50 p-5">
                  <p className="text-sm font-semibold text-slate-700">Señales claras</p>
                  <p className="mt-2 text-sm text-slate-600">Detecta phishing, enlaces extraños y remitentes dudosos.</p>
                </div>
                <div className="rounded-[1.75rem] border border-slate-200 bg-emerald-50 p-5">
                  <p className="text-sm font-semibold text-slate-700">Respuesta rápida</p>
                  <p className="mt-2 text-sm text-slate-600">Obtén resultados en segundos y toma decisiones con confianza.</p>
                </div>
                <div className="rounded-[1.75rem] border border-slate-200 bg-amber-50 p-5">
                  <p className="text-sm font-semibold text-slate-700">Soporte suave</p>
                  <p className="mt-2 text-sm text-slate-600">No necesitas ser experto para saber si algo es dudoso.</p>
                </div>
              </div>
            </section>
            <div>
              <AuthForm mode={mode} onSubmit={handleSubmit} error={error} />
              <div className="mt-4 flex items-center justify-between">
                <button
                  onClick={() => setMode(mode === 'login' ? 'register' : 'login')}
                  className="text-sm text-sky-600 hover:underline"
                >
                  {mode === 'login' ? '¿No tienes cuenta? Regístrate' : '¿Ya tienes cuenta? Inicia sesión'}
                </button>
                <button onClick={handleGuestStart} className="text-sm text-slate-600 hover:underline">
                  Continuar como invitado
                </button>
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-8">
            <section className="grid gap-8 lg:grid-cols-[1fr_0.9fr]">
              <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-[0_30px_60px_rgba(15,23,42,0.08)]">
                <p className="text-sm uppercase tracking-[0.35em] text-slate-500">Bienvenido</p>
                <h2 className="mt-4 text-4xl font-semibold text-slate-950">Hola, {user?.name || 'amigo'}. Listo para revisar otro mensaje?</h2>
                <p className="mt-4 text-base leading-7 text-slate-600">
                  BluePHish está aquí para ayudarte a entender por qué un correo es seguro o necesita una segunda mirada.
                </p>
              </div>

              <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-[0_30px_60px_rgba(15,23,42,0.08)]">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="text-sm uppercase tracking-[0.35em] text-slate-500">Tu espacio</p>
                    <p className="mt-2 text-2xl font-semibold text-slate-950">Resumen rápido</p>
                  </div>
                  {token && !isGuest && (
                    <button
                      onClick={handleLogout}
                      className="rounded-full border border-slate-200 bg-slate-50 px-4 py-3 text-sm font-semibold text-slate-700 transition hover:border-slate-300"
                    >
                      <LogOut className="mr-2 inline-block h-4 w-4" />
                      Cerrar sesión
                    </button>
                  )}
                </div>
                <div className="mt-6 grid gap-4 sm:grid-cols-3">
                  <div className="rounded-[1.75rem] bg-sky-50 p-4 text-center">
                    <p className="text-sm text-slate-600">Análisis</p>
                    <p className="mt-3 text-3xl font-semibold text-slate-950">{history.length}</p>
                  </div>
                  <div className="rounded-[1.75rem] bg-emerald-50 p-4 text-center">
                    <p className="text-sm text-slate-600">Confianza</p>
                    <p className="mt-3 text-3xl font-semibold text-slate-950">{history.length ? (history.reduce((sum, item) => sum + item.score, 0) / history.length).toFixed(1) : '0'}</p>
                  </div>
                  <div className="rounded-[1.75rem] bg-amber-50 p-4 text-center">
                    <p className="text-sm text-slate-600">Alertas</p>
                    <p className="mt-3 text-3xl font-semibold text-slate-950">{history.filter((item) => item.risk_level === 'high').length}</p>
                  </div>
                </div>
              </div>
            </section>

            <EmailAnalysisForm onAnalyze={handleAnalyze} isLoading={isAnalyzing} result={analysisResult} />

            <section className="grid gap-8 lg:grid-cols-2">
              {token ? (
                <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-[0_30px_60px_rgba(15,23,42,0.08)]">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="text-sm uppercase tracking-[0.35em] text-slate-500">Historial</p>
                    <h2 className="mt-2 text-3xl font-semibold text-slate-950">Tus últimos análisis</h2>
                  </div>
                </div>
                <p className="mt-4 text-sm leading-6 text-slate-600">Guarda tus resultados y vuelve cuando necesites revisar otro correo.</p>
                <div className="mt-6">
                  <HistoryList entries={history} />
                </div>
              </div>

              ) : (
                <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-[0_30px_60px_rgba(15,23,42,0.08)]">
                  <div>
                    <p className="text-sm uppercase tracking-[0.35em] text-slate-500">Invitado</p>
                    <h2 className="mt-2 text-3xl font-semibold text-slate-950">Modo invitado</h2>
                  </div>
                  <p className="mt-4 text-sm leading-6 text-slate-600">Estás en modo invitado: los análisis no se guardarán en el historial.</p>
                </div>
              )}
                {token && (
                  <>
                    <div>
                      <p className="text-sm uppercase tracking-[0.35em] text-slate-500">Confianza</p>
                      <h2 className="mt-2 text-3xl font-semibold text-slate-950">¿Cómo se ve tu seguridad?</h2>
                    </div>
                    <p className="mt-4 text-sm leading-6 text-slate-600">Una vista simple de qué mensajes son seguros y cuáles merecen precaución.</p>
                    <div className="mt-6">
                      <RiskDistributionChart entries={history} />
                    </div>
                  </>
                )}
            </section>

            {token && <AdminPanel token={token} />}
          </div>
        )}
      </main>
      <footer className="mt-6 border-t border-slate-200 bg-transparent py-4 text-center">
        <div className="max-w-7xl mx-auto px-6 text-sm text-slate-500">by david A roa v.</div>
      </footer>
    </div>
  )
}

export default App
