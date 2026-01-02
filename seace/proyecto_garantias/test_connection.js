import mysql from 'mysql2/promise';

async function testConnection() {
    try {
        console.log('🔍 Probando conexión a MySQL...\n');

        const connection = await mysql.createConnection({
            host: 'localhost',
            user: 'root',
            password: '123456789',
            database: 'garantias_seace'
        });

        console.log('✅ Conexión exitosa!\n');

        // Probar consulta
        const [rows] = await connection.execute('SELECT COUNT(*) as total FROM Licitaciones_Cabecera');
        console.log('📊 Total de registros en Licitaciones_Cabecera:', rows[0].total);

        const [rows2] = await connection.execute('SELECT COUNT(*) as total FROM Licitaciones_Adjudicaciones');
        console.log('📊 Total de registros en Licitaciones_Adjudicaciones:', rows2[0].total);

        await connection.end();
        console.log('\n✅ Test completado exitosamente!');

    } catch (error) {
        console.error('❌ Error:', error.message);
        process.exit(1);
    }
}

testConnection();
