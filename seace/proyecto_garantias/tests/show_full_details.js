import pool from '../backend/config/database.js';

async function showFullManualDetails() {
    console.log('🔍 Buscando la última licitación MANUAL en la base de datos...');
    try {
        // 1. Get latest header
        const [headers] = await pool.query(`
            SELECT * FROM licitaciones_cabecera 
            WHERE origen_tipo = 'MANUAL' 
            ORDER BY fecha_creacion DESC 
            LIMIT 1
        `);

        if (headers.length === 0) {
            console.log("❌ No se encontraron licitaciones con origen_tipo = 'MANUAL'");
            process.exit(0);
        }

        const header = headers[0];
        console.log('\n=== TABLA: licitaciones_cabecera ===');
        console.log(`ID Convocatoria: ${header.id_convocatoria}`);
        console.log(`Descripción:     ${header.descripcion}`);
        console.log(`Fecha Creación:  ${header.fecha_creacion}`);
        console.log(`Origen:          ${header.origen_tipo}`);

        // 2. Get adjudicaciones
        const [adjudicaciones] = await pool.query(`
            SELECT * FROM licitaciones_adjudicaciones 
            WHERE id_convocatoria = ?
        `, [header.id_convocatoria]);

        console.log('\n=== TABLA: licitaciones_adjudicaciones ===');
        if (adjudicaciones.length === 0) console.log("   (Sin adjudicaciones registradas)");

        for (const adj of adjudicaciones) {
            console.log(`   - ID Adj:      ${adj.id_adjudicacion}`);
            console.log(`     Ganador:     ${adj.ganador_nombre}`);
            console.log(`     Monto:       ${adj.monto_adjudicado}`);
            console.log(`     Garantía:    ${adj.tipo_garantia}`);
            console.log(`     Estado:      ${adj.estado_item}`);

            // 3. Get consorcios
            const [consorcios] = await pool.query(`
                 SELECT * FROM consorcios 
                 WHERE id_contrato = ?
            `, [adj.id_contrato]);

            if (consorcios.length > 0) {
                console.log('     === TABLA: consorcios ===');
                consorcios.forEach(c => console.log(`        * Miembro: ${c.nombre_miembro} (${c.porcentaje_participacion}%)`));
            }
        }

    } catch (error) {
        console.error('❌ Error de consulta:', error.message);
    }
    process.exit(0);
}

showFullManualDetails();
