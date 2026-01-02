import pool from '../backend/config/database.js';

async function checkLatestManual() {
    console.log('🔍 Checking latest MANUAL licitacion...');
    try {
        const [rows] = await pool.query(`
            SELECT id_convocatoria, nomenclatura, origen_tipo, fecha_creacion, estado_proceso 
            FROM licitaciones_cabecera 
            ORDER BY fecha_creacion DESC 
            LIMIT 5
        `);
        console.table(rows);
    } catch (error) {
        console.error('❌ Error:', error.message);
    }
    process.exit(0);
}

checkLatestManual();
