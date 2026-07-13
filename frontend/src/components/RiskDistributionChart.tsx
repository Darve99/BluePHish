interface HistoryEntry {
  id: number
  created_at: string
  subject: string
  score: number
  risk_level: string
  summary: string
}

interface RiskDistributionChartProps {
  entries: HistoryEntry[]
}

export function RiskDistributionChart({ entries }: RiskDistributionChartProps) {
  const calculateDistribution = () => {
    if (entries.length === 0) {
      return { high: 0, medium: 0, low: 0, total: 0 }
    }

    const high = entries.filter((e) => e.risk_level === 'high').length
    const medium = entries.filter((e) => e.risk_level === 'medium').length
    const low = entries.filter((e) => e.risk_level === 'low').length
    const total = entries.length

    return { high, medium, low, total }
  }

  const distribution = calculateDistribution()

  if (distribution.total === 0) {
    return (
      <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6">
        <p className="text-sm uppercase tracking-[0.3em] text-cyan-400">Distribución</p>
        <h3 className="mt-2 text-xl font-semibold text-white">Riesgos detectados</h3>
        <p className="mt-6 text-center text-sm text-slate-400">Sin datos aún. Realiza tu primer análisis.</p>
      </div>
    )
  }

  const highPercent = Math.round((distribution.high / distribution.total) * 100)
  const mediumPercent = Math.round((distribution.medium / distribution.total) * 100)
  const lowPercent = Math.round((distribution.low / distribution.total) * 100)

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6">
      <div>
        <p className="text-sm uppercase tracking-[0.3em] text-cyan-400">Distribución</p>
        <h3 className="mt-2 text-xl font-semibold text-white">Riesgos detectados</h3>
      </div>

      <div className="mt-6 space-y-4">
        {/* High Risk */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-red-500"></div>
              <span className="text-sm font-medium text-white">Riesgo Alto</span>
            </div>
            <span className="text-sm text-red-400 font-semibold">
              {distribution.high} ({highPercent}%)
            </span>
          </div>
          <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-red-500 transition-all duration-500"
              style={{ width: `${highPercent}%` }}
            ></div>
          </div>
        </div>

        {/* Medium Risk */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-orange-500"></div>
              <span className="text-sm font-medium text-white">Riesgo Medio</span>
            </div>
            <span className="text-sm text-orange-400 font-semibold">
              {distribution.medium} ({mediumPercent}%)
            </span>
          </div>
          <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-orange-500 transition-all duration-500"
              style={{ width: `${mediumPercent}%` }}
            ></div>
          </div>
        </div>

        {/* Low Risk */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-green-500"></div>
              <span className="text-sm font-medium text-white">Riesgo Bajo</span>
            </div>
            <span className="text-sm text-green-400 font-semibold">
              {distribution.low} ({lowPercent}%)
            </span>
          </div>
          <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-green-500 transition-all duration-500"
              style={{ width: `${lowPercent}%` }}
            ></div>
          </div>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-3 gap-3">
        <div className="rounded-lg bg-slate-950 p-3 text-center">
          <p className="text-xs text-slate-400">Total</p>
          <p className="mt-1 text-2xl font-bold text-white">{distribution.total}</p>
        </div>
        <div className="rounded-lg bg-red-950/20 p-3 text-center">
          <p className="text-xs text-red-400">Altos</p>
          <p className="mt-1 text-2xl font-bold text-red-400">{distribution.high}</p>
        </div>
        <div className="rounded-lg bg-green-950/20 p-3 text-center">
          <p className="text-xs text-green-400">Bajos</p>
          <p className="mt-1 text-2xl font-bold text-green-400">{distribution.low}</p>
        </div>
      </div>
    </div>
  )
}
