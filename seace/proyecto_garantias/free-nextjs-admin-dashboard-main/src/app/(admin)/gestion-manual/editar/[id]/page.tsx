
import EditarLicitacionClient from './client';

export async function generateStaticParams() {
    console.log('Generating params for gestion-manual');
    return [{ id: '1' }];
}

export default function EditarLicitacionPage() {
    return <EditarLicitacionClient />;
}
