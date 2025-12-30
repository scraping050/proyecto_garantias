'use client'

import { useState, useEffect, Suspense } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { useLicitaciones } from '@/hooks/use-licitaciones'
import { BankBadge } from '@/components/data/bank-badge'
import { StatusBadge } from '@/components/data/status-badge'
import { formatCurrency, formatDate } from '@/lib/formatters'
import { Search, Copy, ExternalLink, ChevronLeft, ChevronRight } from 'lucide-react'
import { debounce, copyToClipboard } from '@/lib/utils'
import Link from 'next/link'

export default function LicitacionesPage() {
    return (
        <Suspense fallback={<div>Cargando...</div>}>
            <LicitacionesContent />
        </Suspense>
    )
}

function LicitacionesContent() {
    const router = useRouter()
    const searchParams = useSearchParams()

    // Get filters from URL
    const page = parseInt(searchParams?.get('page') || '1')
    const limit = parseInt(searchParams?.get('limit') || '20')
    const searchQuery = searchParams?.get('search') || ''

    const [search, setSearch] = useState(searchQuery)

    // Fetch data with filters
    const { data, isLoading, error } = useLicitaciones({
        page,
        limit,
    })

    // Debounced search
    useEffect(() => {
        const debouncedSearch = debounce(() => {
            const params = new URLSearchParams(searchParams?.toString() || '')
            if (search) {
                params.set('search', search)
            } else {
                params.delete('search')
            }
            params.set('page', '1') // Reset to page 1 on search
            router.push(`/licitaciones?${params.toString()}`)
        }, 500)

        debouncedSearch()
    }, [search])

    const updatePage = (newPage: number) => {
        const params = new URLSearchParams(searchParams?.toString() || '')
        params.set('page', newPage.toString())
        router.push(`/licitaciones?${params.toString()}`)
    }

    const updateLimit = (newLimit: number) => {
        const params = new URLSearchParams(searchParams?.toString() || '')
        params.set('limit', newLimit.toString())
        params.set('page', '1')
        router.push(`/licitaciones?${params.toString()}`)
    }

    const handleCopyNomenclatura = async (nomenclatura: string) => {
        const success = await copyToClipboard(nomenclatura)
        if (success) {
            // You can add a toast notification here
            console.log('Nomenclatura copiada')
        }
    }

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold tracking-tight">Licitaciones</h1>
                <p className="text-muted-foreground">
                    Explorador de procesos de licitación con filtros avanzados
                </p>
            </div>

            {/* Filters */}
            <Card>
                <CardHeader>
                    <CardTitle>Filtros</CardTitle>
                    <CardDescription>Busca y filtra licitaciones</CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="flex gap-4">
                        <div className="relative flex-1">
                            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                            <Input
                                placeholder="Buscar por nomenclatura, RUC o entidad..."
                                value={search}
                                onChange={(e) => setSearch(e.target.value)}
                                className="pl-10"
                            />
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* Data Table */}
            <Card>
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <div>
                            <CardTitle>Resultados</CardTitle>
                            <CardDescription>
                                {data ? `${data.total} licitaciones encontradas` : 'Cargando...'}
                            </CardDescription>
                        </div>
                        <div className="flex items-center gap-2">
                            <span className="text-sm text-muted-foreground">Mostrar:</span>
                            <select
                                value={limit}
                                onChange={(e) => updateLimit(parseInt(e.target.value))}
                                className="h-9 rounded-md border border-input bg-background px-3 text-sm"
                            >
                                <option value="10">10</option>
                                <option value="20">20</option>
                                <option value="50">50</option>
                                <option value="100">100</option>
                            </select>
                        </div>
                    </div>
                </CardHeader>
                <CardContent>
                    {isLoading && (
                        <div className="space-y-2">
                            {[...Array(5)].map((_, i) => (
                                <div key={i} className="h-16 animate-pulse rounded-lg bg-muted" />
                            ))}
                        </div>
                    )}

                    {error && (
                        <div className="text-center py-8 text-destructive">
                            Error al cargar las licitaciones
                        </div>
                    )}

                    {data && data.items.length === 0 && (
                        <div className="text-center py-8 text-muted-foreground">
                            No se encontraron licitaciones
                        </div>
                    )}

                    {data && data.items.length > 0 && (
                        <div className="space-y-2">
                            {/* Table Header */}
                            <div className="grid grid-cols-12 gap-4 px-4 py-2 text-sm font-medium text-muted-foreground border-b">
                                <div className="col-span-3">Nomenclatura</div>
                                <div className="col-span-3">Comprador</div>
                                <div className="col-span-2">Monto</div>
                                <div className="col-span-2">Estado</div>
                                <div className="col-span-2">Fecha</div>
                            </div>

                            {/* Table Rows */}
                            {data.items.map((item) => (
                                <div
                                    key={item.id_convocatoria}
                                    className="grid grid-cols-12 gap-4 px-4 py-3 rounded-lg border hover:bg-accent transition-colors"
                                >
                                    <div className="col-span-3 flex items-center gap-2">
                                        <Link
                                            href={`/licitaciones/${item.id_convocatoria}`}
                                            className="font-medium hover:underline truncate"
                                        >
                                            {item.nomenclatura || 'N/A'}
                                        </Link>
                                        <Button
                                            variant="ghost"
                                            size="icon"
                                            className="h-6 w-6 flex-shrink-0"
                                            onClick={() => handleCopyNomenclatura(item.nomenclatura || '')}
                                        >
                                            <Copy className="h-3 w-3" />
                                        </Button>
                                    </div>
                                    <div className="col-span-3 flex items-center truncate text-sm">
                                        {item.comprador || 'N/A'}
                                    </div>
                                    <div className="col-span-2 flex items-center font-medium">
                                        {formatCurrency(item.monto_estimado)}
                                    </div>
                                    <div className="col-span-2 flex items-center">
                                        <StatusBadge status={item.estado_proceso} />
                                    </div>
                                    <div className="col-span-2 flex items-center text-sm text-muted-foreground">
                                        {formatDate(item.fecha_publicacion)}
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}

                    {/* Pagination */}
                    {data && data.total_pages > 1 && (
                        <div className="flex items-center justify-between pt-4">
                            <div className="text-sm text-muted-foreground">
                                Página {data.page} de {data.total_pages}
                            </div>
                            <div className="flex items-center gap-2">
                                <Button
                                    variant="outline"
                                    size="sm"
                                    onClick={() => updatePage(page - 1)}
                                    disabled={page <= 1}
                                >
                                    <ChevronLeft className="h-4 w-4 mr-1" />
                                    Anterior
                                </Button>
                                <Button
                                    variant="outline"
                                    size="sm"
                                    onClick={() => updatePage(page + 1)}
                                    disabled={page >= data.total_pages}
                                >
                                    Siguiente
                                    <ChevronRight className="h-4 w-4 ml-1" />
                                </Button>
                            </div>
                        </div>
                    )}
                </CardContent>
            </Card>
        </div>
    )
}
