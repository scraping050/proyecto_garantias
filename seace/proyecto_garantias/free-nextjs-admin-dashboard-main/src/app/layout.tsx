import { Outfit } from 'next/font/google';
import './globals.css';

import { Providers } from './providers';
import type { Metadata } from 'next';

const outfit = Outfit({
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: 'Dashboard SEACE - Análisis de Licitaciones MCQS',
  description: 'Panel avanzado para el seguimiento y análisis de licitaciones del SEACE. Herramientas de inteligencia de negocios para la gestión de oportunidades con el Estado.',
  keywords: ["SEACE", "Licitaciones", "Contrataciones con el Estado", "OSCE", "Inteligencia de Negocios", "MCQS"],
  authors: [{ name: "MCQS" }],
  icons: {
    icon: '/images/logo/mqs-logo.jpg',
  },
  openGraph: {
    title: "Dashboard SEACE - Análisis de Licitaciones MCQS",
    description: "Monitoree y analice licitaciones públicas en tiempo real.",
    type: "website",
    siteName: "MCQS Analytics",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${outfit.className} dark:bg-gray-900`} suppressHydrationWarning>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}
