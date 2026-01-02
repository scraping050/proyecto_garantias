// Utilidades para exportación de reportes
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';

export interface ExportData {
    columns: { key: string; label: string }[];
    data: any[];
    title: string;
    subtitle?: string;
    filters?: Record<string, string>;
}

const THEME_COLOR = [37, 99, 235] as [number, number, number]; // Blue-600
const SECONDARY_COLOR = [100, 116, 139] as [number, number, number]; // Slate-500

/**
 * Generate a strictly safe filename
 * Format: Prefix_YYYYMMDDHHMMSS.ext
 */
const getSafeFilename = (prefix: string, ext: string) => {
    const timestamp = new Date().toISOString().replace(/[-:T.]/g, '').slice(0, 14);
    // Remove anything that isn't a letter, number, or underscore/hyphen
    const safePrefix = prefix.replace(/[^a-zA-Z0-9\-_]/g, '_');
    const filename = `${safePrefix}_${timestamp}.${ext}`;
    console.log(`Generating safe filename: ${filename}`);
    return filename;
};

/**
 * Exporta datos a PDF con Diseño Profesional
 */
export const exportToPDF = (exportData: ExportData) => {
    const orientation = exportData.columns.length > 6 ? 'landscape' : 'portrait';
    const doc = new jsPDF({ orientation });
    const pageWidth = doc.internal.pageSize.width;

    // --- Header ---
    doc.setFillColor(THEME_COLOR[0], THEME_COLOR[1], THEME_COLOR[2]);
    doc.rect(0, 0, pageWidth, 5, 'F');

    doc.setFontSize(22);
    doc.setFont("helvetica", "bold");
    doc.setTextColor(30, 41, 59);
    doc.text(exportData.title, 14, 22);

    let yPos = 30;

    if (exportData.subtitle) {
        doc.setFontSize(11);
        doc.setFont("helvetica", "normal");
        doc.setTextColor(SECONDARY_COLOR[0], SECONDARY_COLOR[1], SECONDARY_COLOR[2]);
        doc.text(exportData.subtitle, 14, yPos);
        yPos += 8;
    }

    const fecha = new Date().toLocaleString('es-PE');

    doc.setFontSize(10);
    doc.setTextColor(100);

    doc.setFillColor(248, 250, 252);
    doc.setDrawColor(226, 232, 240);
    doc.roundedRect(14, yPos, pageWidth - 28, 12, 1, 1, 'FD');

    doc.text(`Generado: ${fecha}`, 18, yPos + 8);
    doc.text(`Total registros: ${exportData.data.length}`, pageWidth - 18, yPos + 8, { align: 'right' });

    yPos += 18;

    // --- Table ---
    const headers = exportData.columns.map(col => col.label);
    const rows = exportData.data.map(row =>
        exportData.columns.map(col => {
            const val = row[col.key];
            if (val === null || val === undefined) return '-';
            if (typeof val === 'number') return val.toLocaleString('es-PE');
            return String(val);
        })
    );

    autoTable(doc, {
        head: [headers],
        body: rows,
        startY: yPos,
        theme: 'grid',
        styles: { fontSize: 9, cellPadding: 3, textColor: [51, 65, 85], lineColor: [226, 232, 240], lineWidth: 0.1, valign: 'middle' },
        headStyles: { fillColor: [255, 255, 255], textColor: [15, 23, 42], fontStyle: 'bold', lineColor: [203, 213, 225], lineWidth: 0.1 },
        alternateRowStyles: { fillColor: [248, 250, 252] },
        didDrawPage: (data) => {
            const pageCount = doc.getNumberOfPages();
            doc.setFontSize(8);
            doc.setTextColor(148, 163, 184);
            const footerText = `Sistema de Garantías SEACE - Página ${pageCount}`;
            doc.text(footerText, pageWidth / 2, doc.internal.pageSize.height - 10, { align: 'center' });
        }
    });

    // Use native jsPDF save for PDF
    const filename = getSafeFilename('Reporte', 'pdf');
    doc.save(filename);
};

/**
 * Exporta datos a Excel
 */
export const exportToExcel = (exportData: ExportData) => {
    const metadata = [
        [exportData.title.toUpperCase()],
        [exportData.subtitle || ''],
        [''],
        ['Fecha Generación', new Date().toLocaleString('es-PE')],
        ['Total Registros', exportData.data.length],
        ['']
    ];

    const headers = exportData.columns.map(col => col.label);
    const rows = exportData.data.map(row => exportData.columns.map(col => row[col.key] ?? ''));
    const wsData = [...metadata, headers, ...rows];

    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.aoa_to_sheet(wsData);
    const colWidths = headers.map(h => ({ wch: Math.max(h.length + 5, 20) }));
    ws['!cols'] = colWidths;
    XLSX.utils.book_append_sheet(wb, ws, 'Reporte');

    // Excel is fine with saveAs
    const wbout = XLSX.write(wb, { bookType: 'xlsx', type: 'array' });
    const blob = new Blob([wbout], { type: 'application/octet-stream' });
    const filename = getSafeFilename('Reporte', 'xlsx');
    saveAs(blob, filename);
};

/**
 * Exporta datos a CSV
 */
export const exportToCSV = (exportData: ExportData) => {
    const headers = exportData.columns.map(col => col.label).join(',');
    const rows = exportData.data.map(row =>
        exportData.columns.map(col => {
            const value = row[col.key] ?? '';
            const strVal = String(value);
            if (strVal.includes(',') || strVal.includes('"') || strVal.includes('\n')) {
                return `"${strVal.replace(/"/g, '""')}"`;
            }
            return strVal;
        }).join(',')
    );

    const csvContent = '\uFEFF' + [headers, ...rows].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const filename = getSafeFilename('Reporte', 'csv');
    saveAs(blob, filename);
};

/**
 * Exporta una Licitación individual a PDF
 */
export const exportLicitacionToPDF = (licitacion: any) => {
    const doc = new jsPDF();
    const lineHeight = 7;
    let y = 20;

    const addLine = (label: string, value: any) => {
        if (!value) return;
        if (y > 270) { doc.addPage(); y = 20; }
        doc.setFont("helvetica", "bold");
        doc.text(`${label}:`, 14, y);
        doc.setFont("helvetica", "normal");
        const splitText = doc.splitTextToSize(String(value), 120);
        doc.text(splitText, 50, y);
        y += (splitText.length * lineHeight);
    };

    const addSection = (title: string) => {
        y += 5;
        if (y > 270) { doc.addPage(); y = 20; }
        doc.setFont("helvetica", "bold");
        doc.setFontSize(12);
        doc.setTextColor(37, 99, 235);
        doc.text(title, 14, y);
        doc.setTextColor(0);
        doc.setFontSize(10);
        y += 10;
        doc.setDrawColor(200);
        doc.line(14, y - 8, 196, y - 8);
    };

    doc.setFontSize(16);
    doc.setTextColor(37, 99, 235);
    const title = licitacion.nomenclatura || `Licitación ${licitacion.id_convocatoria}`;
    const splitTitle = doc.splitTextToSize(title, 180);
    doc.text(splitTitle, 14, y);
    y += (splitTitle.length * 8) + 10;

    doc.setFontSize(10);
    doc.setTextColor(0);

    addSection("Información General");
    addLine("ID Convocatoria", licitacion.id_convocatoria);
    addLine("Descripción", licitacion.descripcion);
    addLine("Estado", licitacion.estado_proceso);
    addLine("Categoría", licitacion.categoria);

    addSection("Comprador");
    addLine("Entidad", licitacion.comprador);

    addSection("Ubicación");
    addLine("Departamento", licitacion.departamento);
    addLine("Provincia", licitacion.provincia);
    addLine("Distrito", licitacion.distrito);

    addSection("Montos y Fechas");
    if (licitacion.monto_estimado) addLine("Monto Estimado", new Intl.NumberFormat('es-PE', { style: 'currency', currency: 'PEN' }).format(licitacion.monto_estimado));
    if (licitacion.monto_total_adjudicado) addLine("Monto Adjudicado", new Intl.NumberFormat('es-PE', { style: 'currency', currency: 'PEN' }).format(licitacion.monto_total_adjudicado));
    if (licitacion.fecha_publicacion) addLine("Fecha Publicación", new Date(licitacion.fecha_publicacion).toLocaleDateString('es-PE'));

    if (licitacion.ganadores) {
        addSection("Adjudicación");
        addLine("Ganadores", licitacion.ganadores);
        addLine("RUCs", licitacion.ganadores_ruc);
        addLine("Entidad Fin.", licitacion.entidades_financieras);
        addLine("Garantías", licitacion.tipos_garantia);
    }

    const pageCount = doc.getNumberOfPages();
    for (let i = 1; i <= pageCount; i++) {
        doc.setPage(i);
        doc.setFontSize(8);
        doc.setTextColor(150);
        doc.text(`Generado el ${new Date().toLocaleString('es-PE')} - Sistema de Garantías SEACE`, 14, 285);
        doc.text(`Página ${i} de ${pageCount}`, 196, 285, { align: 'right' });
    }

    // Use native jsPDF save with safe filename
    // Extract ID for prefix but keep it safe
    const safePrefix = `Licitacion_${licitacion.id_convocatoria}`.replace(/[^a-zA-Z0-9\-_]/g, '_');
    const filename = getSafeFilename(safePrefix, 'pdf');
    doc.save(filename);
};
