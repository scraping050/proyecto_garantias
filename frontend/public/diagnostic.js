// Paste this in browser console after logging in to diagnose the issue

console.log('=== DIAGNOSTIC REPORT ===');

const userStr = localStorage.getItem('user');
console.log('\n1. Raw user data from localStorage:');
console.log(userStr);

if (userStr) {
    const user = JSON.parse(userStr);
    console.log('\n2. Parsed user object:');
    console.log(user);

    console.log('\n3. Field verification:');
    console.log('  - perfil:', user.perfil || 'MISSING');
    console.log('  - job_title:', user.job_title || 'MISSING');
    console.log('  - nombre:', user.nombre || 'MISSING');
    console.log('  - email:', user.email || 'MISSING');

    console.log('\n4. Expected values for Diana:');
    console.log('  - perfil should be: DIRECTOR');
    console.log('  - job_title should be: Asistente de operaciones');

    console.log('\n5. Actual vs Expected:');
    console.log('  - perfil:', user.perfil === 'DIRECTOR' ? '✅ CORRECT' : '❌ WRONG');
    console.log('  - job_title:', user.job_title === 'Asistente de operaciones' ? '✅ CORRECT' : '❌ WRONG');
} else {
    console.log('❌ No user data in localStorage - please login first');
}

console.log('\n=== END REPORT ===');
