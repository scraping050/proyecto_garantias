const { exec } = require('child_process');

console.log('🔄 Reiniciando servicios...');

// Kill existing node processes
exec('taskkill /F /IM node.exe', (error, stdout, stderr) => {
    if (error) {
        console.warn('⚠️ No se pudieron matar procesos Node (quizás no había ninguno):', error.message);
    } else {
        console.log('✅ Procesos Node detenidos.');
    }

    console.log('🚀 Iniciando Backend...');
    const backend = exec('start cmd /k "npm run dev"', { cwd: 'c:\\laragon\\www\\proyecto_garantias\\backend' });
    backend.unref();

    console.log('🚀 Iniciando Frontend...');
    const frontend = exec('start cmd /k "npm run dev"', { cwd: 'c:\\laragon\\www\\proyecto_garantias\\free-nextjs-admin-dashboard-main' });
    frontend.unref();

    console.log('✨ Reinicio completado. Las nuevas ventanas deberían abrirse.');
});
