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
    <form onSubmit={handleSubmit} className="space-y-6 rounded-[2rem] border border-slate-200 bg-white p-8 shadow-[0_30px_60px_rgba(15,23,42,0.08)]">
      <div>
        <p className="text-sm uppercase tracking-[0.28em] text-slate-500">Acceso seguro</p>
        <h2 className="mt-2 text-3xl font-semibold text-slate-950">{mode === 'login' ? 'Iniciar sesión' : 'Crear cuenta'}</h2>
        <p className="mt-2 text-sm text-slate-600">
          {mode === 'login' ? 'Ingresa para consultar tu historial y revisar correos.' : 'Regístrate para comenzar a proteger tu bandeja de entrada.'}
        </p>
      </div>

      {mode === 'register' && (
        <label className="block text-sm text-slate-700">
          <span className="mb-2 block text-slate-900">Nombre</span>
          <input
            className="w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-sky-400 focus:ring-2 focus:ring-sky-200"
            value={name}
            onChange={(event) => setName(event.target.value)}
            required
          />
        </label>
      )}

      <label className="block text-sm text-slate-700">
        <span className="mb-2 block text-slate-900">Correo</span>
        <input
          type="email"
          className="w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-sky-400 focus:ring-2 focus:ring-sky-200"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          required
        />
      </label>

      <label className="block text-sm text-slate-700">
        <span className="mb-2 block text-slate-900">Contraseña</span>
        <input
          type="password"
          className="w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-sky-400 focus:ring-2 focus:ring-sky-200"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          required
        />
      </label>

      {error && <p className="text-sm text-rose-500">{error}</p>}

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full rounded-full bg-sky-600 px-5 py-3 text-base font-semibold text-white transition hover:bg-sky-500 disabled:cursor-not-allowed disabled:opacity-70"
      >
        {isSubmitting ? 'Procesando...' : mode === 'login' ? 'Entrar' : 'Registrarme'}
      </button>
    </form>
  )
}
