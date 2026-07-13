interface HistoryEntry {
  id: number
  created_at: string
  subject: string
  score: number
  risk_level: string
  summary: string
}

interface AnalysisTrendProps {
  entries: HistoryEntry[]
}

export function AnalysisTrend({ entries }: AnalysisTrendProps) {
  const calculateDailyTrend = () => {
    if (entries.length === 0) {
      return { days: [], counts: [], avgScores: [] }
    }

    // Group entries by day
    const dayMap = new Map<string, { count: number; totalScore: number }>()

    entries.forEach((entry) => {
      const date = new Date(entry.created_at)
      const dayKey = date.toLocaleDateString('es-ES', { month: 'short', day: 'numeric' })

      if (!dayMap.has(dayKey)) {
        dayMap.set(dayKey, { count: 0, totalScore: 0 })
      }

      const dayData = dayMap.get(dayKey)!
      dayData.count += 1
      dayData.totalScore += entry.score
    })

    // Convert to arrays for display (last 7 days)
    const days = Array.from(dayMap.keys()).slice(-7)
    const counts = days.map((day) => dayMap.get(day)?.count || 0)
    const avgScores = days.map((day) => {
      const dayData = dayMap.get(day)
      return dayData ? Math.round(dayData.totalScore / dayData.count) : 0
    })

    return { days, counts, avgScores }
  }

  const trend = calculateDailyTrend()
  const maxCount = Math.max(...trend.counts, 1)

  if (trend.days.length === 0) {
    return (
      <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6">
        <p className="text-sm uppercase tracking-[0.3em] text-cyan-400">Tendencia</p>
        <h3 className="mt-2 text-xl font-semibold text-white">Actividad reciente</h3>
        <p className="mt-6 text-center text-sm text-slate-400">Sin datos aún.</p>
      </div>
    )
  }

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6">
      <div>
        <p className="text-sm uppercase tracking-[0.3em] text-cyan-400">Tendencia</p>
        <h3 className="mt-2 text-xl font-semibold text-white">Actividad reciente</h3>
      </div>

      <div className="mt-6">
        <div className="flex items-end justify-between gap-2 h-32">
          {trend.days.map((day, idx) => {
            const heightPercent = (trend.counts[idx] / maxCount) * 100
            const avgScore = trend.avgScores[idx]
            const color =
              avgScore >= 70 ? 'bg-red-500' : avgScore >= 40 ? 'bg-orange-500' : 'bg-green-500'

            return (
              <div key={day} className="flex flex-1 flex-col items-center gap-2">
                <div
                  className={`${color} w-full transition-all duration-300 rounded-t opacity-70 hover:opacity-100`}
                  style={{ height: `${heightPercent || 5}%` }}
                  title={`${trend.counts[idx]} análisis, riesgo promedio: ${avgScore}`}
                ></div>
                <span className="text-xs text-slate-500">{day}</span>
              </div>
            )
          })}
        </div>
      </div>

      <div className="mt-6 grid grid-cols-3 gap-3 text-center text-xs">
        <div className="rounded-lg bg-slate-950 p-2">
          <p className="text-slate-400">Hoy</p>
          <p className="mt-1 text-lg font-semibold text-cyan-400">{trend.counts[trend.counts.length - 1]}</p>
        </div>
        <div className="rounded-lg bg-slate-950 p-2">
          <p className="text-slate-400">Promedio</p>
          <p className="mt-1 text-lg font-semibold text-orange-400">
            {Math.round(trend.counts.reduce((a, b) => a + b, 0) / trend.counts.length)}
          </p>
        </div>
        <div className="rounded-lg bg-slate-950 p-2">
          <p className="text-slate-400">Total</p>
          <p className="mt-1 text-lg font-semibold text-white">{trend.counts.reduce((a, b) => a + b, 0)}</p>
        </div>
      </div>
    </div>
  )
}
