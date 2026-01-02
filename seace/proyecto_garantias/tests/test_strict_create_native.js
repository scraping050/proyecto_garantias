
async function testStrictCreate() {
    console.log('🧪 Starting Strict Value Verification (Native Fetch)...');

    const payload = {
        descripcion: "TEST VALIDACION ESTRICTA - NATIVE",
        comprador: "ENTIDAD DE PRUEBA 2",
        departamento: "AREQUIPA",
        provincia: "AREQUIPA",
        distrito: "CERCADO",
        estado_proceso: "CONTRATADO",
        categoria: "BIENES",
        monto_estimado: 75000.00,
        fecha_publicacion: new Date().toISOString().split('T')[0],
        moneda: "PEN",
        tipo_procedimiento: "Subasta Inversa Electrónica",
        adjudicaciones: [
            {
                ganador_nombre: "PROVEEDOR MODELO EIRL",
                ganador_ruc: "20202020202",
                monto_adjudicado: 70000.00,
                fecha_adjudicacion: new Date().toISOString().split('T')[0],
                // CRITICAL FIELDS TO TEST:
                estado_item: "CONSENTIDO",
                tipo_garantia: "POLIZA DE CAUCION",
                entidad_financiera: "MAPFRE PERU COMPAÑIA DE SEGUROS Y REASEGUROS"
            }
        ]
    };

    try {
        const response = await fetch('http://localhost:5000/api/licitaciones/crear', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.status === 201 && data.success) {
            console.log('✅ Success! Licitacion created.');
            console.log(`   ID New: ${data.data.id_convocatoria}`);
            console.log('✅ Backend accepted strict values (Poliza, Consentido, Mapfre).');
        } else {
            console.error('❌ Failed to create licitacion.');
            console.error('   Status:', response.status);
            console.error('   Response:', JSON.stringify(data, null, 2));
        }

    } catch (error) {
        console.error('❌ Network or Script Error:', error.message);
    }
}

testStrictCreate();
