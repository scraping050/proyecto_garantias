import pool from '../backend/config/database.js';

async function checkCabeceraSchema() {
    console.log('🔍 Inspecting Schema for licitaciones_cabecera...');
    try {
        const [columns] = await pool.query(`DESCRIBE licitaciones_cabecera`);
        console.log('Columns found:');
        columns.forEach(c => console.log(` - ${c.Field} (${c.Type})`));
    } catch (error) {
        console.error('❌ Error describing table:', error.message);
    }
    process.exit(0);
}

checkCabeceraSchema();
