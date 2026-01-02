import pool from '../backend/config/database.js';

async function addFechaAdjudicacion() {
    console.log('🔧 Adding column `fecha_adjudicacion` to `licitaciones_cabecera`...');
    try {
        await pool.query(`
            ALTER TABLE licitaciones_cabecera 
            ADD COLUMN fecha_adjudicacion DATE DEFAULT NULL AFTER fecha_publicacion
        `);
        console.log('✅ Column added successfully.');
    } catch (error) {
        if (error.code === 'ER_DUP_FIELDNAME') {
            console.log('⚠️ Column already exists.');
        } else {
            console.error('❌ Error altering table:', error.message);
        }
    }
    process.exit(0);
}

addFechaAdjudicacion();
