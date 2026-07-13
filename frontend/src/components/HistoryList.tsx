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
    <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-cyan-400">Historial</p>
          <h3 className="mt-2 text-xl font-semibold text-white">Análisis recientes</h3>
        </div>
      </div>

      {entries.length === 0 ? (
        <p className="mt-4 text-sm text-slate-400">Aún no hay análisis guardados.</p>
      ) : (
        <ul className="mt-4 space-y-3">
          {entries.map((entry) => (
            <li key={entry.id} className="rounded-xl border border-slate-800 bg-slate-950 p-4">
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="font-medium text-white">{entry.subject || 'Sin asunto'}</p>
                  <p className="mt-1 text-sm text-slate-400">{new Date(entry.created_at).toLocaleString()}</p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-cyan-400">{entry.score}/100</p>
                  <p className="text-sm text-slate-400">{entry.risk_level}</p>
                </div>
              </div>
              <p className="mt-3 text-sm text-slate-300">{entry.summary}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
