export const formatEntityName = (nombre: string): string => {
    if (!nombre) return '';
    const nombreUpper = nombre.toUpperCase();

    // Check for cooperatives FIRST (before checking for "CREDITO" which would match BCP)
    if (nombreUpper.includes('COOPERATIVA')) return 'Coop. San Lorenzo'; // Or generic 'Coop.' if multiple exist? 
    // Wait, hardcoding 'Coop. San Lorenzo' is risky if there are others. 
    // Better logic: Replace "COOPERATIVA DE AHORRO Y CREDITO" with "COOP."

    if (nombreUpper.includes('COOPERATIVA')) {
        return nombre
            .replace(/COOPERATIVA DE AHORRO Y CREDITO/i, 'COOP.')
            .replace(/COOPERATIVA DE AHORRO Y CRÉDITO/i, 'COOP.')
            .replace(/COOPERATIVA/i, 'COOP.'); // Fallback
    }

    if (nombreUpper.includes('AVLA')) return 'AVLA Perú';
    if (nombreUpper.includes('CESCE')) return 'CESCE Perú';
    if (nombreUpper.includes('BBVA')) return 'BBVA Perú';
    if (nombreUpper.includes('CREDITO') && nombreUpper.includes('BANCO')) return 'BCP';
    if (nombreUpper.includes('BCP')) return 'BCP';
    if (nombreUpper.includes('CRECER')) return 'Crecer Seguros';
    if (nombreUpper.includes('SCOTIABANK')) return 'Scotiabank';
    if (nombreUpper.includes('INSUR')) return 'Insur Seguros';
    if (nombreUpper.includes('INTERAMERICANO')) return 'Interamericano';
    if (nombreUpper.includes('CITIBANK')) return 'Citibank';
    if (nombreUpper.includes('INTERNACIONAL')) return 'Internacional';
    if (nombreUpper.includes('FOGAPI')) return 'FOGAPI';
    if (nombreUpper.includes('SANTANDER')) return 'Santander';
    if (nombreUpper.includes('PICHINCHA')) return 'Pichincha';
    if (nombreUpper.includes('MAPFRE')) return 'Mapfre';
    if (nombreUpper.includes('POSITIVA')) return 'La Positiva';

    // CMAC logic
    if (nombreUpper.includes('CMAC')) {
        // Try to extract the city name if possible, or just return the existing name if it's already short
        return nombre;
    }

    return nombre;
};
