import pool from '../backend/config/database.js';

async function testQueries() {
    console.log('Testing Filter Queries...');

    try {
        console.log('1. Testing Departamentos...');
        const [deptos] = await pool.query(`
            SELECT DISTINCT departamento 
            FROM licitaciones_cabecera 
            WHERE departamento IS NOT NULL 
            ORDER BY departamento
        `);
        console.log(`   ✅ Success. Found ${deptos.length} departamentos.`);
    } catch (error) {
        console.error('   ❌ FAILED Departamentos:', error.message);
    }

    try {
        console.log('2. Testing Estados...');
        const [estados] = await pool.query(`
            SELECT DISTINCT estado_proceso 
            FROM licitaciones_cabecera 
            WHERE estado_proceso IS NOT NULL 
            ORDER BY estado_proceso
        `);
        console.log(`   ✅ Success. Found ${estados.length} estados.`);
    } catch (error) {
        console.error('   ❌ FAILED Estados:', error.message);
    }

    try {
        console.log('3. Testing Compradores...');
        const [compradores] = await pool.query(`
            SELECT DISTINCT comprador 
            FROM licitaciones_cabecera 
            WHERE comprador IS NOT NULL 
            ORDER BY comprador
            LIMIT 10
        `);
        console.log(`   ✅ Success. Found ${compradores.length} compradores.`);
    } catch (error) {
        console.error('   ❌ FAILED Compradores:', error.message);
    }

    process.exit(0);
}

testQueries();
