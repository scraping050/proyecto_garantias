import pool from '../backend/config/database.js';

async function checkSchema() {
    console.log('🔍 Inspecting Schema for licitaciones_adjudicaciones...');
    try {
        const [columns] = await pool.query(`DESCRIBE licitaciones_adjudicaciones`);
        console.log('Columns found:');
        columns.forEach(c => console.log(` - ${c.Field} (${c.Type})`));
    } catch (error) {
        console.error('❌ Error describing table:', error.message);
    }
    process.exit(0);
}

checkSchema();
