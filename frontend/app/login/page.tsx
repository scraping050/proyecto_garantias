'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

export default function LoginPage() {
    const router = useRouter()
    const [credentials, setCredentials] = useState({
        id_corporativo: '',
        password: ''
    })
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError('')
        setLoading(true)

        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(credentials),
            })

            if (!response.ok) {
                throw new Error('Credenciales incorrectas')
            }

            const data = await response.json()

            // Store token and user data
            localStorage.setItem('token', data.access_token)
            localStorage.setItem('user', JSON.stringify(data.user))

            // Redirect to modules selection
            router.push('/modules')
        } catch (err) {
            setError('Credenciales incorrectas. Intente nuevamente.')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center p-6">
            <div className="bg-white rounded-lg shadow-2xl p-12 max-w-md w-full">
                <div className="text-center space-y-4 mb-10">
                    <h1 className="text-4xl font-bold text-gray-900 tracking-wide">
                        IDENTIFICACIÓN
                    </h1>
                    <p className="text-gray-600 text-sm tracking-wide">
                        Acceso seguro al entorno MQS
                    </p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label className="block text-xs font-bold text-gray-700 mb-2 tracking-wider uppercase">
                            ID Corporativo
                        </label>
                        <Input
                            type="text"
                            placeholder="Usuario"
                            value={credentials.id_corporativo}
                            onChange={(e) => setCredentials({ ...credentials, id_corporativo: e.target.value })}
                            className="bg-gray-50 border-gray-300 h-12"
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-xs font-bold text-gray-700 mb-2 tracking-wider uppercase">
                            Clave de Acceso
                        </label>
                        <Input
                            type="password"
                            placeholder="••••••••"
                            value={credentials.password}
                            onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
                            className="bg-gray-50 border-gray-300 h-12"
                            required
                        />
                    </div>

                    {error && (
                        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded text-sm">
                            {error}
                        </div>
                    )}

                    <Button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-[#1e3a5f] hover:bg-[#2a4a7f] text-white py-6 text-sm font-bold tracking-widest uppercase shadow-lg"
                    >
                        {loading ? 'INICIANDO...' : 'INICIAR SESIÓN'}
                    </Button>
                </form>

                <div className="mt-8 text-center">
                    <Link href="/" className="text-sm text-gray-600 hover:text-gray-900 tracking-wide uppercase font-medium">
                        Volver
                    </Link>
                </div>
            </div>
        </div>
    )
}
