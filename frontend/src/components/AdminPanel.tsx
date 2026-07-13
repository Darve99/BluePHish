import { useEffect, useState } from 'react'

interface Rule { id: string; name: string; weight: number }
interface Stats { total_users: number; total_rules: number; last_analysis_score: number }

interface AdminPanelProps {
  token: string | null
}

export function AdminPanel({ token }: AdminPanelProps) {
  const [rules, setRules] = useState<Rule[]>([])
  const [stats, setStats] = useState<Stats | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadAdminData = async () => {
      if (!token) return
      try {
        const [rulesResponse, statsResponse] = await Promise.all([
          fetch(`${import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'}/admin/rules`, {
            headers: { Authorization: `Bearer ${token}` },
          }),
          fetch(`${import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'}/admin/stats`, {
            headers: { Authorization: `Bearer ${token}` },
          }),
        ])

        if (rulesResponse.ok) {
          setRules(await rulesResponse.json())
        }
        if (statsResponse.ok) {
          setStats(await statsResponse.json())
        }
      } catch {
        setError('No se pudieron cargar los datos de administración')
      }
    }

    void loadAdminData()
  }, [token])

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6">
      <p className="text-sm uppercase tracking-[0.3em] text-cyan-400">Administración</p>
      <h3 className="mt-2 text-xl font-semibold text-white">Panel de control</h3>
      {error && <p className="mt-3 text-sm text-rose-400">{error}</p>}

      {stats && (
        <div className="mt-4 grid gap-4 md:grid-cols-3">
          <div className="rounded-xl border border-slate-800 bg-slate-950 p-4">
            <p className="text-sm text-slate-400">Usuarios</p>
            <p className="mt-2 text-2xl font-semibold text-white">{stats.total_users}</p>
          </div>
          <div className="rounded-xl border border-slate-800 bg-slate-950 p-4">
            <p className="text-sm text-slate-400">Reglas</p>
            <p className="mt-2 text-2xl font-semibold text-white">{stats.total_rules}</p>
          </div>
          <div className="rounded-xl border border-slate-800 bg-slate-950 p-4">
            <p className="text-sm text-slate-400">Última puntuación</p>
            <p className="mt-2 text-2xl font-semibold text-white">{stats.last_analysis_score}</p>
          </div>
        </div>
      )}

      <div className="mt-6">
        <h4 className="text-sm font-semibold text-slate-200">Reglas configurables</h4>
        <ul className="mt-3 space-y-2">
          {rules.map((rule) => (
            <li key={rule.id} className="rounded-lg border border-slate-800 bg-slate-950 px-3 py-2 text-sm text-slate-300">
              {rule.name}: <span className="text-cyan-400">{rule.weight}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
