'use client';

import type { Metadata } from "next";
import { Montserrat } from "next/font/google";
import "./globals.css";
import Script from "next/script";
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState } from 'react';
import { AuthProvider } from '@/contexts/auth-context';
import { SettingsProvider } from '@/contexts/settings-context';

const montserrat = Montserrat({ subsets: ["latin"], weight: ["300", "400", "500", "600", "700", "800"] });

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    const [queryClient] = useState(() => new QueryClient({
        defaultOptions: {
            queries: {
                staleTime: 60 * 1000, // 1 minute
                refetchOnWindowFocus: false,
            },
        },
    }));

    return (
        <html lang="es">
            <head>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
            </head>
            <body className={montserrat.className}>
                <QueryClientProvider client={queryClient}>
                    <AuthProvider>
                        <SettingsProvider>
                            {children}
                        </SettingsProvider>
                    </AuthProvider>
                </QueryClientProvider>
                <Script src="https://cdn.jsdelivr.net/npm/chart.js" strategy="beforeInteractive" />
            </body>
        </html>
    );
}
