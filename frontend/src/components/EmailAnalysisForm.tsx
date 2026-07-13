import { ChangeEvent, FormEvent, useState } from 'react'

interface EmailAnalysisFormProps {
  onAnalyze: (rawEmail: string, file?: File | null) => Promise<void>
  isLoading?: boolean
  result?: {
    subject?: string
    from?: string
    to?: string
    score?: number
    risk_level?: string
    summary?: string
    indicators?: Array<{ detail: string }>
    urls?: string[]
  } | null
}

export function EmailAnalysisForm({ onAnalyze, isLoading = false, result }: EmailAnalysisFormProps) {
  const [rawEmail, setRawEmail] = useState('')
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
    await onAnalyze(rawEmail, selectedFile)
  }

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] || null
    setSelectedFile(file)
    if (file) {
      void onAnalyze('', file)
    }
  }

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6">
        <label className="block text-sm text-slate-300">
          <span className="mb-2 block">Pega el correo sospechoso</span>
          <textarea
            className="min-h-[240px] w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-3 text-sm text-slate-200 outline-none"
            value={rawEmail}
            onChange={(event) => setRawEmail(event.target.value)}
            placeholder="Subject: ...\nFrom: ...\nTo: ...\n\nEste es un ejemplo de correo sospechoso"
          />
        </label>
        <div className="mt-4 flex flex-wrap items-center gap-3">
          <button
            type="submit"
            disabled={isLoading}
            className="rounded-lg bg-cyan-500 px-4 py-2 font-medium text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-70"
          >
            {isLoading ? 'Analizando...' : 'Analizar correo'}
          </button>
          <label className="cursor-pointer rounded-lg border border-slate-700 px-4 py-2 text-sm text-slate-300 transition hover:border-cyan-500">
            <span>{selectedFile ? selectedFile.name : 'Subir .eml'}</span>
            <input type="file" accept=".eml" className="hidden" onChange={handleFileChange} />
          </label>
        </div>
      </form>

      {result && (
        <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6">
          <p className="text-sm uppercase tracking-[0.3em] text-cyan-400">Resultado</p>
          <div className="mt-4 grid gap-4 md:grid-cols-2">
            <div>
              <p className="text-sm text-slate-400">Asunto</p>
              <p className="text-white">{result.subject || 'No detectado'}</p>
            </div>
            <div>
              <p className="text-sm text-slate-400">Remitente</p>
              <p className="text-white">{result.from || 'No detectado'}</p>
            </div>
          </div>
          <div className="mt-4 rounded-xl border border-slate-800 bg-slate-950 p-4">
            <p className="text-sm text-slate-400">Puntuación</p>
            <p className="text-3xl font-semibold text-white">{result.score ?? 0}/100</p>
            <p className="mt-2 text-sm text-cyan-400">Nivel: {result.risk_level || 'low'}</p>
            <p className="mt-3 text-sm text-slate-300">{result.summary}</p>
          </div>
          <div className="mt-4">
            <p className="text-sm text-slate-400">Indicadores</p>
            <ul className="mt-2 space-y-2 text-sm text-slate-300">
              {result.indicators?.map((indicator, index) => (
                <li key={`${indicator.detail}-${index}`} className="rounded-lg border border-slate-800 bg-slate-950 px-3 py-2">
                  {indicator.detail}
                </li>
              ))}
            </ul>
          </div>
          {result.urls && result.urls.length > 0 && (
            <div className="mt-4">
              <p className="text-sm text-slate-400">URLs detectadas</p>
              <ul className="mt-2 space-y-2 text-sm text-slate-300">
                {result.urls.map((url) => (
                  <li key={url} className="break-all rounded-lg border border-slate-800 bg-slate-950 px-3 py-2">
                    {url}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
