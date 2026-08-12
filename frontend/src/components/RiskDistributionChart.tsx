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
      return { high: 0, medium: 0, low: 0, none: 0, total: 0 }
    }

    const high = entries.filter((e) => e.risk_level === 'high').length
    const medium = entries.filter((e) => e.risk_level === 'medium').length
    const low = entries.filter((e) => e.risk_level === 'low').length
    const none = entries.filter((e) => e.risk_level === 'none').length
    const total = entries.length

    return { high, medium, low, none, total }
  }

  const distribution = calculateDistribution()

  if (distribution.total === 0) {
    return (
      <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6 shadow-sm">
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Distribución</p>
        <h3 className="mt-2 text-xl font-semibold text-slate-950">Riesgos detectados</h3>
        <p className="mt-6 text-center text-sm text-slate-600">Sin datos aún. Realiza tu primer análisis.</p>
      </div>
    )
  }

  const highPercent = Math.round((distribution.high / distribution.total) * 100)
  const mediumPercent = Math.round((distribution.medium / distribution.total) * 100)
  const lowPercent = Math.round((distribution.low / distribution.total) * 100)
  const nonePercent = Math.round((distribution.none / distribution.total) * 100)

  return (
    <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6 shadow-sm">
      <div>
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Distribución</p>
        <h3 className="mt-2 text-xl font-semibold text-slate-950">Riesgos detectados</h3>
      </div>

      <div className="mt-6 space-y-4">
        {/* High Risk */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-red-500"></div>
              <span className="text-sm font-medium text-slate-950">Riesgo Alto</span>
            </div>
            <span className="text-sm text-red-600 font-semibold">
              {distribution.high} ({highPercent}%)
            </span>
          </div>
          <div className="w-full h-2 bg-slate-200 rounded-full overflow-hidden">
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
              <div className="w-3 h-3 rounded-full bg-amber-500"></div>
              <span className="text-sm font-medium text-slate-950">Riesgo Medio</span>
            </div>
            <span className="text-sm text-amber-600 font-semibold">
              {distribution.medium} ({mediumPercent}%)
            </span>
          </div>
          <div className="w-full h-2 bg-slate-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-amber-500 transition-all duration-500"
              style={{ width: `${mediumPercent}%` }}
            ></div>
          </div>
        </div>

        {/* Low Risk */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-emerald-500"></div>
              <span className="text-sm font-medium text-slate-950">Riesgo Bajo</span>
            </div>
            <span className="text-sm text-emerald-600 font-semibold">
              {distribution.low} ({lowPercent}%)
            </span>
          </div>
          <div className="w-full h-2 bg-slate-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-emerald-500 transition-all duration-500"
              style={{ width: `${lowPercent}%` }}
            ></div>
          </div>
        </div>

        {/* None Risk */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-slate-500"></div>
              <span className="text-sm font-medium text-slate-950">Riesgo Nulo</span>
            </div>
            <span className="text-sm text-slate-600 font-semibold">
              {distribution.none} ({nonePercent}%)
            </span>
          </div>
          <div className="w-full h-2 bg-slate-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-slate-500 transition-all duration-500"
              style={{ width: `${nonePercent}%` }}
            ></div>
          </div>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-4 gap-3">
        <div className="rounded-lg bg-white p-3 text-center shadow-sm">
          <p className="text-xs text-slate-500">Total</p>
          <p className="mt-1 text-2xl font-bold text-slate-950">{distribution.total}</p>
        </div>
        <div className="rounded-lg bg-red-50 p-3 text-center">
          <p className="text-xs text-red-600">Altos</p>
          <p className="mt-1 text-2xl font-bold text-red-600">{distribution.high}</p>
        </div>
        <div className="rounded-lg bg-amber-50 p-3 text-center">
          <p className="text-xs text-amber-600">Medios</p>
          <p className="mt-1 text-2xl font-bold text-amber-600">{distribution.medium}</p>
        </div>
        <div className="rounded-lg bg-slate-100 p-3 text-center">
          <p className="text-xs text-slate-500">Nulos</p>
          <p className="mt-1 text-2xl font-bold text-slate-950">{distribution.none}</p>
        </div>
      </div>
    </div>
  )
}
