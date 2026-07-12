import { FormEvent, useState } from 'react'

interface AuthFormProps {
  mode: 'login' | 'register'
  onSubmit: (payload: { name?: string; email: string; password: string }) => Promise<void>
  error?: string | null
}

export function AuthForm({ mode, onSubmit, error }: AuthFormProps) {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
    setIsSubmitting(true)
    try {
      await onSubmit({ name: mode === 'register' ? name : undefined, email, password })
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 rounded-2xl border border-slate-800 bg-slate-900/80 p-6">
      <div>
        <h2 className="text-xl font-semibold text-white">
          {mode === 'login' ? 'Iniciar sesión' : 'Crear cuenta'}
        </h2>
        <p className="mt-1 text-sm text-slate-400">
          {mode === 'login' ? 'Accede a tu panel de análisis' : 'Regístrate para empezar a analizar correos'}
        </p>
      </div>

      {mode === 'register' && (
        <label className="block text-sm text-slate-300">
          <span className="mb-1 block">Nombre</span>
          <input
            className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm outline-none ring-0"
            value={name}
            onChange={(event) => setName(event.target.value)}
            required
          />
        </label>
      )}

      <label className="block text-sm text-slate-300">
        <span className="mb-1 block">Correo</span>
        <input
          type="email"
          className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm outline-none ring-0"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          required
        />
      </label>

      <label className="block text-sm text-slate-300">
        <span className="mb-1 block">Contraseña</span>
        <input
          type="password"
          className="w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm outline-none ring-0"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          required
        />
      </label>

      {error && <p className="text-sm text-rose-400">{error}</p>}

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full rounded-lg bg-cyan-500 px-4 py-2 font-medium text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-70"
      >
        {isSubmitting ? 'Procesando...' : mode === 'login' ? 'Entrar' : 'Registrarme'}
      </button>
    </form>
  )
}
