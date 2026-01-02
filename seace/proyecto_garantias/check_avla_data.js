import pool from './backend/config/database.js';

async function checkData() {
    try {
        console.log("🔍 Checking AVLA and Cooperativa data...\n");

        // 1. Raw DB Count
        const [rows] = await pool.query(`
            SELECT entidad_financiera, COUNT(*) as count 
            FROM licitaciones_adjudicaciones 
            WHERE entidad_financiera LIKE '%AVLA%' 
               OR entidad_financiera LIKE '%COOPERATIVA%'
            GROUP BY entidad_financiera
        `);

        console.log("📊 RAW DB COUNTS:");
        console.table(rows);

        // 2. Report API check (simulating request)
        // We want to see if the 'por-entidad-financiera' endpoint returns them
        const [apiRows] = await pool.query(`
             SELECT 
                CASE 
                    WHEN a.entidad_financiera LIKE '%COOPERATIVA%' THEN 'Coop. San Lorenzo'
                    WHEN a.entidad_financiera LIKE '%AVLA%' THEN 'AVLA Perú'
                    ELSE a.entidad_financiera 
                END as entidad_normalizada,
                COUNT(a.id_adjudicacion) as total
            FROM licitaciones_adjudicaciones a
            WHERE entidad_financiera IS NOT NULL AND entidad_financiera != '' AND entidad_financiera != 'SIN_GARANTIA'
            GROUP BY entidad_normalizada
            HAVING entidad_normalizada IN ('AVLA Perú', 'Coop. San Lorenzo')
        `);

        console.log("\n📊 API AGGREGATION SIMULATION:");
        console.table(apiRows);

        process.exit(0);
    } catch (error) {
        console.error("Error:", error);
        process.exit(1);
    }
}

checkData();
