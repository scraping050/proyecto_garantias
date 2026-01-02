import pool from '../backend/config/database.js';

async function auditData() {
    console.log('🕵️‍♂️ Auditing DB Content for User Explanation...');

    try {
        // 1. Current Distinct Values for tipo_garantia
        const [tipos] = await pool.query(`
            SELECT DISTINCT tipo_garantia, COUNT(*) as c 
            FROM licitaciones_adjudicaciones 
            GROUP BY tipo_garantia
        `);
        console.log('\n=== VALORES ACTUALES EN TIPO_GARANTIA ===');
        tipos.forEach(t => console.log(`"${t.tipo_garantia}": ${t.c}`));

        // 2. Search for "CARTA FIANZA" or "POLIZA" in entidad_financiera
        const [matches] = await pool.query(`
            SELECT entidad_financiera 
            FROM licitaciones_adjudicaciones 
            WHERE entidad_financiera LIKE '%CARTA FIANZA%' 
               OR entidad_financiera LIKE '%POLIZA%' 
               OR entidad_financiera LIKE '%CAUCION%'
            LIMIT 10
        `);
        console.log('\n=== BUSQUEDA DE PALABRAS CLAVE EN ENTIDAD ===');
        if (matches.length > 0) {
            matches.forEach(m => console.log(`Found in entity: ${m.entidad_financiera}`));
        } else {
            console.log('No matches found for generic terms in entidad_financiera.');
        }

    } catch (error) {
        console.error(error);
    }
    process.exit(0);
}

auditData();
