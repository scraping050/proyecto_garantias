import pool from '../backend/config/database.js';

async function applyIndexes() {
    console.log('🚀 Applying Database Indexes for Performance...');

    const indexes = [
        "CREATE INDEX idx_licitaciones_origen ON licitaciones_cabecera(origen_tipo)",
        "CREATE INDEX idx_licitaciones_estado ON licitaciones_cabecera(estado_proceso)",
        "CREATE INDEX idx_licitaciones_fecha ON licitaciones_cabecera(fecha_publicacion)",
        "CREATE INDEX idx_licitaciones_departamento ON licitaciones_cabecera(departamento)"
    ];

    for (const query of indexes) {
        try {
            await pool.query(query);
            console.log(`✅ Index applied: ${query}`);
        } catch (error) {
            if (error.code === 'ER_DUP_KEYNAME') {
                console.log(`⚠️ Index already exists: ${query}`);
            } else {
                console.error(`❌ Error applying index: ${error.message}`);
            }
        }
    }

    console.log('🏁 Indexing process completed.');
    process.exit(0);
}

applyIndexes();
