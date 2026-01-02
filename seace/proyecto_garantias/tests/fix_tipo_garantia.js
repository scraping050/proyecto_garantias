import pool from '../backend/config/database.js';

async function fixTipoGarantia() {
    console.log('🔧 Converting `tipo_garantia` from GENERATED to NORMAL column...');
    try {
        // First drop the generated status by modifying the column
        // We preserve VARCHAR(50) and make it explicitly NOT generated.
        await pool.query(`
            ALTER TABLE licitaciones_adjudicaciones 
            MODIFY COLUMN tipo_garantia VARCHAR(50) DEFAULT NULL
        `);
        console.log('✅ Column modified successfully. It should now be mutable.');
    } catch (error) {
        console.error('❌ Error altering table:', error.message);
    }
    process.exit(0);
}

fixTipoGarantia();
