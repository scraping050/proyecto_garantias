import pool from '../backend/config/database.js';

async function showCreateTable() {
    console.log('🔍 Showing Create Table for licitaciones_adjudicaciones...');
    try {
        const [rows] = await pool.query(`SHOW CREATE TABLE licitaciones_adjudicaciones`);
        console.log(rows[0]['Create Table']);
    } catch (error) {
        console.error('❌ Error:', error.message);
    }
    process.exit(0);
}

showCreateTable();
