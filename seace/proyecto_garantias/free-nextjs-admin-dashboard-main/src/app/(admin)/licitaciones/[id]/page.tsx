
import LicitacionClient from './client';

export async function generateStaticParams() {
    console.log('Generating params for licitaciones');
    return [{ id: '1' }];
}

export default async function LicitacionPage({ params }: { params: Promise<{ id: string }> }) {
    const { id } = await params;
    return <LicitacionClient id={id} />;
}
