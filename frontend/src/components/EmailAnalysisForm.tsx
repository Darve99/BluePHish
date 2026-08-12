import { ChangeEvent, FormEvent, useState } from 'react'

interface EmailAnalysisFormProps {
  onAnalyze: (rawEmail: string, file?: File | null, subject?: string, hasAttachment?: boolean) => Promise<void>
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
  const [subject, setSubject] = useState('')
  const [hasAttachment, setHasAttachment] = useState(false)

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
    await onAnalyze(rawEmail, selectedFile, subject, hasAttachment)
  }

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] || null
    setSelectedFile(file)
    if (file) {
      // uploading a file implies it contains the email; mark attachment true
      void onAnalyze('', file, '', true)
    }
  }

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit} className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-[0_30px_60px_rgba(15,23,42,0.08)]">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Escaneo</p>
            <h2 className="mt-2 text-2xl font-semibold text-slate-950">Revisa un correo</h2>
          </div>
          <span className="rounded-full bg-slate-100 px-4 py-2 text-sm text-slate-700">Texto o archivo .eml</span>
        </div>

        <label className="block text-sm text-slate-700">
          <span className="mb-3 block text-slate-900">Pega el correo sospechoso</span>
          <textarea
            className="min-h-[280px] w-full rounded-[1.5rem] border border-slate-200 bg-slate-50 px-4 py-4 text-sm text-slate-900 outline-none transition focus:border-sky-400 focus:ring-2 focus:ring-sky-100"
            value={rawEmail}
            onChange={(event) => setRawEmail(event.target.value)}
            placeholder="Subject: ...\nFrom: ...\nTo: ...\n\nEste es un mensaje que quiero revisar"
          />
        </label>

        <label className="block text-sm text-slate-700 mt-4">
          <span className="mb-2 block text-slate-900">Asunto (opcional, para entrada manual)</span>
          <input
            className="w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-sky-400 focus:ring-2 focus:ring-sky-100"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            placeholder="Asunto del correo"
          />
        </label>

        <label className="inline-flex items-center gap-2 mt-3 text-sm text-slate-700">
          <input type="checkbox" checked={hasAttachment} onChange={(e) => setHasAttachment(e.target.checked)} />
          <span>El correo tiene archivo adjunto</span>
        </label>

        <div className="flex flex-wrap items-center gap-3">
          <button
            type="submit"
            disabled={isLoading}
            className="rounded-full bg-sky-600 px-5 py-3 text-base font-semibold text-white transition hover:bg-sky-500 disabled:cursor-not-allowed disabled:opacity-70"
          >
            {isLoading ? 'Analizando...' : 'Iniciar análisis'}
          </button>
          <label className="cursor-pointer rounded-full border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-700 transition hover:border-sky-400 hover:text-slate-900">
            <span>{selectedFile ? selectedFile.name : 'Subir archivo .eml'}</span>
            <input type="file" accept=".eml" className="hidden" onChange={handleFileChange} />
          </label>
        </div>
      </form>

      {result && (
        <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-[0_30px_60px_rgba(15,23,42,0.08)]">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Resultado</p>
              <h2 className="mt-2 text-2xl font-semibold text-slate-950">Riesgo detectado</h2>
            </div>
            <span className="rounded-full bg-slate-100 px-4 py-2 text-sm text-slate-700">{result.score ?? 0}/100</span>
          </div>

          <div className="mt-6 grid gap-6 lg:grid-cols-2">
            <div className="rounded-[1.5rem] border border-slate-200 bg-slate-50 p-5">
              <p className="text-sm text-slate-500">Asunto</p>
              <p className="mt-2 text-lg font-semibold text-slate-950">{result.subject || 'No detectado'}</p>
            </div>
            <div className="rounded-[1.5rem] border border-slate-200 bg-slate-50 p-5">
              <p className="text-sm text-slate-500">Remitente</p>
              <p className="mt-2 text-lg font-semibold text-slate-950">{result.from || 'No detectado'}</p>
            </div>
          </div>

          <div className="mt-6 rounded-[1.5rem] border border-slate-200 bg-slate-50 p-5">
            <p className="text-sm text-slate-500">Nivel de riesgo</p>
            <p className="mt-3 text-4xl font-bold text-slate-950">{result.risk_level || 'low'}</p>
            <p className="mt-4 text-sm leading-6 text-slate-600">{result.summary}</p>
          </div>

          <div className="mt-6 grid gap-4">
            {result.indicators && result.indicators.length > 0 && (
              <div className="rounded-[1.5rem] border border-slate-200 bg-slate-50 p-5">
                <p className="text-sm text-slate-500">Indicadores</p>
                <ul className="mt-3 space-y-2 text-sm text-slate-700">
                  {result.indicators.map((indicator, index) => (
                    <li key={`${indicator.detail}-${index}`} className="rounded-2xl border border-slate-200 bg-white px-3 py-2">
                      {indicator.detail}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {result.urls && result.urls.length > 0 && (
              <div className="rounded-[1.5rem] border border-slate-200 bg-slate-50 p-5">
                <p className="text-sm text-slate-500">URLs detectadas</p>
                <ul className="mt-3 space-y-2 text-sm text-slate-700">
                  {result.urls.map((url) => (
                    <li key={url} className="break-all rounded-2xl border border-slate-200 bg-white px-3 py-2">
                      {url}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
