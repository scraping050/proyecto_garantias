'use client'

import { use } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useLicitacionDetail } from '@/hooks/use-licitaciones'
import { BankBadge } from '@/components/data/bank-badge'
import { StatusBadge } from '@/components/data/status-badge'
import { formatCurrency, formatDate, formatRUC, formatPercent } from '@/lib/formatters'
import { Copy, ExternalLink, ArrowLeft } from 'lucide-react'
import { copyToClipboard } from '@/lib/utils'
import Link from 'next/link'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'
import type { Consorcio } from '@/types'

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8']

export default function LicitacionDetailPage({
    params,
}: {
    params: { id: string }
}) {
    const id = parseInt(params.id)
    const { data: licitacion, isLoading, error } = useLicitacionDetail(id)

    if (isLoading) {
        return (
            <div className="space-y-6">
                <div className="h-8 w-64 animate-pulse bg-muted rounded" />
                <div className="grid gap-6 md:grid-cols-3">
                    <div className="md:col-span-2 space-y-4">
                        {[...Array(3)].map((_, i) => (
                            <Card key={i}>
                                <CardHeader>
                                    <div className="h-6 w-32 animate-pulse bg-muted rounded" />
                                </CardHeader>
                                <CardContent>
                                    <div className="space-y-2">
                                        <div className="h-4 w-full animate-pulse bg-muted rounded" />
                                        <div className="h-4 w-3/4 animate-pulse bg-muted rounded" />
                                    </div>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </div>
            </div>
        )
    }

    if (error || !licitacion) {
        return (
            <div className="space-y-6">
                <Link href="/licitaciones">
                    <Button variant="ghost" size="sm">
                        <ArrowLeft className="h-4 w-4 mr-2" />
                        Volver
                    </Button>
                </Link>
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-destructive">Licitación no encontrada</p>
                    </CardContent>
                </Card>
            </div>
        )
    }

    const handleCopy = async (text: string) => {
        await copyToClipboard(text)
    }

    // Prepare consortium data for pie chart
    const consortiumData = licitacion.adjudicacion?.consorcios.map((c: Consorcio, index: number) => ({
        name: c.nombre_miembro || 'N/A',
        value: c.porcentaje_participacion || 0,
        fill: COLORS[index % COLORS.length],
    })) || []

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <Link href="/licitaciones">
                    <Button variant="ghost" size="sm">
                        <ArrowLeft className="h-4 w-4 mr-2" />
                        Volver
                    </Button>
                </Link>
            </div>

            {/* Title */}
            <div>
                <div className="flex items-center gap-3 mb-2">
                    <h1 className="text-3xl font-bold tracking-tight">
                        {licitacion.nomenclatura || 'N/A'}
                    </h1>
                    <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => handleCopy(licitacion.nomenclatura || '')}
                    >
                        <Copy className="h-4 w-4" />
                    </Button>
                </div>
                <p className="text-lg text-muted-foreground">
                    {licitacion.comprador || 'N/A'}
                </p>
            </div>

            {/* Main Grid */}
            <div className="grid gap-6 md:grid-cols-3">
                {/* Left Column - Process Details */}
                <div className="md:col-span-2 space-y-4">
                    {/* Status Card */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Estado del Proceso</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="flex items-center justify-between">
                                <span className="text-sm text-muted-foreground">Estado:</span>
                                <StatusBadge status={licitacion.estado_proceso} />
                            </div>
                            <div className="flex items-center justify-between">
                                <span className="text-sm text-muted-foreground">Fecha Publicación:</span>
                                <span className="font-medium">{formatDate(licitacion.fecha_publicacion)}</span>
                            </div>
                            {licitacion.adjudicacion && (
                                <div className="flex items-center justify-between">
                                    <span className="text-sm text-muted-foreground">Fecha Adjudicación:</span>
                                    <span className="font-medium">{formatDate(licitacion.adjudicacion.fecha_adjudicacion)}</span>
                                </div>
                            )}
                        </CardContent>
                    </Card>

                    {/* Contract Details */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Detalles del Contrato</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <span className="text-sm text-muted-foreground block mb-1">Monto Estimado</span>
                                    <span className="text-lg font-bold">{formatCurrency(licitacion.monto_estimado)}</span>
                                </div>
                                {licitacion.adjudicacion && (
                                    <div>
                                        <span className="text-sm text-muted-foreground block mb-1">Monto Adjudicado</span>
                                        <span className="text-lg font-bold text-green-600 dark:text-green-400">
                                            {formatCurrency(licitacion.adjudicacion.monto_adjudicado)}
                                        </span>
                                    </div>
                                )}
                            </div>
                            {licitacion.descripcion && (
                                <div>
                                    <span className="text-sm text-muted-foreground block mb-1">Descripción</span>
                                    <p className="text-sm">{licitacion.descripcion}</p>
                                </div>
                            )}
                            <div className="grid grid-cols-2 gap-4">
                                {licitacion.categoria && (
                                    <div>
                                        <span className="text-sm text-muted-foreground block mb-1">Categoría</span>
                                        <span className="text-sm">{licitacion.categoria}</span>
                                    </div>
                                )}
                                {licitacion.tipo_procedimiento && (
                                    <div>
                                        <span className="text-sm text-muted-foreground block mb-1">Tipo Procedimiento</span>
                                        <span className="text-sm">{licitacion.tipo_procedimiento}</span>
                                    </div>
                                )}
                            </div>
                            {licitacion.ubicacion_completa && (
                                <div>
                                    <span className="text-sm text-muted-foreground block mb-1">Ubicación</span>
                                    <span className="text-sm">{licitacion.ubicacion_completa}</span>
                                </div>
                            )}
                        </CardContent>
                    </Card>
                </div>

                {/* Right Column - Intelligence */}
                <div className="space-y-4">
                    {/* Winner Card */}
                    {licitacion.adjudicacion && (
                        <Card>
                            <CardHeader>
                                <CardTitle>Ganador</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div>
                                    <span className="text-sm text-muted-foreground block mb-1">Proveedor</span>
                                    <span className="font-medium">{licitacion.adjudicacion.ganador_nombre || 'N/A'}</span>
                                </div>
                                <div className="flex items-center justify-between">
                                    <div>
                                        <span className="text-sm text-muted-foreground block mb-1">RUC</span>
                                        <span className="font-mono text-sm">
                                            {formatRUC(licitacion.adjudicacion.ganador_ruc)}
                                        </span>
                                    </div>
                                    <Button
                                        variant="ghost"
                                        size="icon"
                                        onClick={() => handleCopy(licitacion.adjudicacion?.ganador_ruc || '')}
                                    >
                                        <Copy className="h-4 w-4" />
                                    </Button>
                                </div>
                                <div>
                                    <span className="text-sm text-muted-foreground block mb-1">Entidad Financiera</span>
                                    <BankBadge bank={licitacion.adjudicacion.entidad_financiera} />
                                </div>
                            </CardContent>
                        </Card>
                    )}

                    {/* Consortium Structure */}
                    {licitacion.adjudicacion && licitacion.adjudicacion.consorcios.length > 0 && (
                        <Card>
                            <CardHeader>
                                <CardTitle>Estructura del Consorcio</CardTitle>
                                <CardDescription>Análisis generado por IA</CardDescription>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                {/* Pie Chart */}
                                <ResponsiveContainer width="100%" height={200}>
                                    <PieChart>
                                        <Pie
                                            data={consortiumData}
                                            cx="50%"
                                            cy="50%"
                                            labelLine={false}
                                            label={(entry: any) => `${entry.value}%`}
                                            outerRadius={80}
                                            fill="#8884d8"
                                            dataKey="value"
                                        >
                                            {consortiumData.map((entry: { fill: string }, index: number) => (
                                                <Cell key={`cell-${index}`} fill={entry.fill} />
                                            ))}
                                        </Pie>
                                        <Tooltip />
                                    </PieChart>
                                </ResponsiveContainer>

                                {/* Members Table */}
                                <div className="space-y-2">
                                    <div className="text-sm font-medium">Miembros:</div>
                                    {licitacion.adjudicacion.consorcios.map((consorcio: Consorcio, index: number) => (
                                        <div
                                            key={consorcio.id_detalle}
                                            className="flex items-center justify-between p-2 rounded-lg border text-sm"
                                        >
                                            <div className="flex-1">
                                                <div className="font-medium">{consorcio.nombre_miembro || 'N/A'}</div>
                                                <div className="text-xs text-muted-foreground font-mono">
                                                    {formatRUC(consorcio.ruc_miembro)}
                                                </div>
                                            </div>
                                            <div className="flex items-center gap-2">
                                                <div
                                                    className="w-3 h-3 rounded-full"
                                                    style={{ backgroundColor: COLORS[index % COLORS.length] }}
                                                />
                                                <span className="font-bold">
                                                    {formatPercent(consorcio.porcentaje_participacion)}
                                                </span>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </CardContent>
                        </Card>
                    )}
                </div>
            </div>
        </div>
    )
}
