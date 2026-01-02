import pool from '../backend/config/database.js';

async function auditEstadoProceso() {
    console.log('🕵️‍♂️ Auditing Estado Proceso...');

    try {
        const [rows] = await pool.query(`
            SELECT DISTINCT estado_proceso 
            FROM licitaciones_cabecera 
            ORDER BY estado_proceso
        `);
        console.log('\n=== VALORES ENCONTRADOS EN BD ===');
        rows.forEach(r => console.log(`- "${r.estado_proceso}"`));
    } catch (error) {
        console.error(error);
    }
    process.exit(0);
}

auditEstadoProceso();
