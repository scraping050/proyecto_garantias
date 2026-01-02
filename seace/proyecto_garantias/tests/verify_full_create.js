const http = require('http');

const data = JSON.stringify({
    descripcion: "VERIFICACION AUTOMATICA - NO BORRAR - TEST",
    comprador: "ENTIDAD DE PRUEBA 001",
    departamento: "LIMA",
    provincia: "LIMA",
    distrito: "MIRAFLORES",
    estado_proceso: "ADJUDICADO",
    categoria: "SERVICIOS",
    monto_estimado: 9999.99,
    moneda: "PEN",
    tipo_procedimiento: "Licitación Pública",
    fecha_publicacion: "2025-01-01",
    nomenclatura: "TEST-001-2025",
    ocid: "OCID-TEST-001",
    adjudicaciones: [
        {
            ganador_nombre: "CONSORCIO GANADOR TEST",
            ganador_ruc: "20100200300",
            monto_adjudicado: 5000.00,
            fecha_adjudicacion: "2025-01-02",
            estado_item: "ADJUDICADO",
            tipo_garantia: "CARTA FIANZA TEST",
            entidad_financiera: "BANCO TEST",
            id_contrato: "CTR-TEST-001",
            consorcios: [
                { nombre_miembro: "MIEMBRO A", ruc_miembro: "10111222333", porcentaje_participacion: 60 },
                { nombre_miembro: "MIEMBRO B", ruc_miembro: "10444555666", porcentaje_participacion: 40 }
            ]
        }
    ]
});

const options = {
    hostname: 'localhost',
    port: 5000,
    path: '/api/licitaciones/crear',
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Content-Length': data.length
    }
};

const req = http.request(options, (res) => {
    console.log(`STATUS: ${res.statusCode}`);

    let responseData = '';

    res.on('data', (chunk) => {
        responseData += chunk;
    });

    res.on('end', () => {
        console.log('Response Body:', responseData);
        if (res.statusCode === 200) {
            console.log("VERIFICACION EXITOSA: La licitación se creó correctamente en BD.");
        } else {
            console.error("FALLO VERIFICACION: Status no es 200");
        }
    });
});

req.on('error', (e) => {
    console.error(`Problem with request: ${e.message}`);
});

req.write(data);
req.end();
