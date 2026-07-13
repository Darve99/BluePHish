interface HistoryEntry {
  id: number
  created_at: string
  subject: string
  score: number
  risk_level: string
  summary: string
}

interface DashboardMetricsProps {
  entries: HistoryEntry[]
}

export function DashboardMetrics({ entries }: DashboardMetricsProps) {
  const calculateMetrics = () => {
    if (entries.length === 0) {
      return {
        totalAnalyzed: 0,
        averageRisk: '—',
        highRiskCount: 0,
        lastAnalysisTime: '—',
      }
    }

    const totalAnalyzed = entries.length
    const averageRisk = (entries.reduce((sum, e) => sum + e.score, 0) / entries.length).toFixed(1)
    const highRiskCount = entries.filter((e) => e.risk_level === 'high').length
    const lastAnalysis = new Date(entries[0].created_at)
    const now = new Date()
    const diffMs = now.getTime() - lastAnalysis.getTime()
    const diffMins = Math.floor(diffMs / 60000)

    let lastAnalysisTime = 'Hace poco'
    if (diffMins < 1) {
      lastAnalysisTime = 'Justo ahora'
    } else if (diffMins < 60) {
      lastAnalysisTime = `Hace ${diffMins} min`
    } else if (diffMins < 1440) {
      const hours = Math.floor(diffMins / 60)
      lastAnalysisTime = `Hace ${hours}h`
    } else {
      const days = Math.floor(diffMins / 1440)
      lastAnalysisTime = `Hace ${days}d`
    }

    return { totalAnalyzed, averageRisk, highRiskCount, lastAnalysisTime }
  }

  const metrics = calculateMetrics()

  return (
    <div className="grid gap-4 md:grid-cols-4">
      <div className="rounded-xl border border-slate-800 bg-slate-950 p-5 transition hover:border-cyan-500/50">
        <p className="text-sm text-slate-400">Correos analizados</p>
        <p className="mt-3 text-4xl font-bold text-cyan-400">{metrics.totalAnalyzed}</p>
        <p className="mt-2 text-xs text-slate-500">en esta sesión</p>
      </div>

      <div className="rounded-xl border border-slate-800 bg-slate-950 p-5 transition hover:border-cyan-500/50">
        <p className="text-sm text-slate-400">Riesgo promedio</p>
        <p className="mt-3 text-4xl font-bold text-orange-400">{metrics.averageRisk}</p>
        <p className="mt-2 text-xs text-slate-500">/100</p>
      </div>

      <div className="rounded-xl border border-slate-800 bg-slate-950 p-5 transition hover:border-red-500/50">
        <p className="text-sm text-slate-400">Alertas altas</p>
        <p className="mt-3 text-4xl font-bold text-red-400">{metrics.highRiskCount}</p>
        <p className="mt-2 text-xs text-slate-500">riesgo alto</p>
      </div>

      <div className="rounded-xl border border-slate-800 bg-slate-950 p-5 transition hover:border-green-500/50">
        <p className="text-sm text-slate-400">Último análisis</p>
        <p className="mt-3 text-lg font-bold text-green-400">{metrics.lastAnalysisTime}</p>
        <p className="mt-2 text-xs text-slate-500">actualizado</p>
      </div>
    </div>
  )
}
