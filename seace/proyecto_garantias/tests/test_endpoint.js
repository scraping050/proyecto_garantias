async function testEndpoint() {
    console.log('Fetching live endpoint...');
    try {
        const res = await fetch('http://localhost:5000/api/filtros/departamentos');
        console.log('Status:', res.status);
        const text = await res.text();
        console.log('Body:', text.substring(0, 500)); // Show beginning of body
    } catch (err) {
        console.error('Fetch failed:', err.message);
    }
}
testEndpoint();
