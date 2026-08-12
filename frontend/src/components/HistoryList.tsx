interface HistoryEntry {
  id: number
  created_at: string
  subject: string
  score: number
  risk_level: string
  summary: string
}

interface HistoryListProps {
  entries: HistoryEntry[]
}

export function HistoryList({ entries }: HistoryListProps) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6 shadow-sm">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Historial</p>
          <h3 className="mt-2 text-xl font-semibold text-slate-950">Análisis recientes</h3>
        </div>
      </div>

      {entries.length === 0 ? (
        <p className="mt-4 text-sm text-slate-600">Aún no hay análisis guardados.</p>
      ) : (
        <div className="mt-4 max-h-[420px] overflow-y-auto pr-2 scrollbar-soft">
          <ul className="space-y-3">
            {entries.map((entry) => (
              <li key={entry.id} className="rounded-3xl border border-slate-200 bg-white p-4 shadow-sm">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <p className="font-medium text-slate-950">{entry.subject || 'Sin asunto'}</p>
                    <p className="mt-1 text-sm text-slate-500">{new Date(entry.created_at).toLocaleString()}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-sky-600">{entry.score}/100</p>
                    <p className="text-sm text-slate-500">{entry.risk_level}</p>
                  </div>
                </div>
                <p className="mt-3 text-sm text-slate-600">{entry.summary}</p>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
