import pool from '../backend/config/database.js';

async function analyzeFieldValues() {
    console.log('Analyzing Database Values for Form Standardization...');

    try {
        // 1. Tipo Garantía
        const [tipos] = await pool.query(`
            SELECT DISTINCT tipo_garantia, COUNT(*) as count 
            FROM licitaciones_adjudicaciones 
            WHERE tipo_garantia IS NOT NULL AND tipo_garantia != ''
            GROUP BY tipo_garantia
            ORDER BY count DESC
        `);
        console.log('\n=== TIPO GARANTIA ===');
        tipos.forEach(t => console.log(`${t.tipo_garantia} (${t.count})`));

        // 2. Entidad Financiera
        const [entidades] = await pool.query(`
            SELECT DISTINCT entidad_financiera, COUNT(*) as count 
            FROM licitaciones_adjudicaciones 
            WHERE entidad_financiera IS NOT NULL AND entidad_financiera != ''
            GROUP BY entidad_financiera
            ORDER BY count DESC
            LIMIT 50
        `);
        console.log('\n=== ENTIDAD FINANCIERA (Top 50) ===');
        entidades.forEach(e => console.log(`${e.entidad_financiera} (${e.count})`));

        // 3. Estado Item (Just in case)
        const [estados] = await pool.query(`
            SELECT DISTINCT estado_item, COUNT(*) as count 
            FROM licitaciones_adjudicaciones 
            WHERE estado_item IS NOT NULL AND estado_item != ''
            GROUP BY estado_item
            ORDER BY count DESC
        `);
        console.log('\n=== ESTADO ITEM ===');
        estados.forEach(e => console.log(`${e.estado_item} (${e.count})`));

    } catch (error) {
        console.error('❌ Error analyzing fields:', error.message);
    }

    process.exit(0);
}

analyzeFieldValues();
