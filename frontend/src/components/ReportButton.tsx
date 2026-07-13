interface ReportButtonProps {
  onDownload: () => Promise<void>
  isLoading?: boolean
}

export function ReportButton({ onDownload, isLoading = false }: ReportButtonProps) {
  return (
    <button
      onClick={() => void onDownload()}
      disabled={isLoading}
      className="rounded-lg border border-cyan-600 bg-cyan-500/10 px-4 py-2 text-sm font-medium text-cyan-300 transition hover:bg-cyan-500/20 disabled:cursor-not-allowed disabled:opacity-70"
    >
      {isLoading ? 'Generando PDF...' : 'Descargar reporte PDF'}
    </button>
  )
}
