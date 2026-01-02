import type { Metadata } from "next";
import { Montserrat } from "next/font/google";
import "./globals.css";
import Script from "next/script";
import { Providers } from "./providers";

const montserrat = Montserrat({ subsets: ["latin"], weight: ["300", "400", "500", "600", "700", "800"] });

export const metadata: Metadata = {
    title: "Sistema de Gestión de Garantías y Obras - MCQS",
    description: "Plataforma integral para la gestión de garantías, cartas fianza y seguimiento de obras públicas y privadas en Perú. Soluciones avanzadas para el sector construcción.",
    keywords: ["Sistema de Garantías", "MCQS", "Gestión de Obras", "Cartas Fianza", "Licitaciones Peru", "SEACE", "Construcción"],
    authors: [{ name: "MCQS" }, { name: "Yanfranco" }],
    openGraph: {
        title: "Sistema de Gestión de Garantías y Obras - MCQS",
        description: "Optimice el control de sus obras y garantías contractuales con nuestra plataforma especializada.",
        type: "website",
        locale: "es_PE",
        siteName: "MCQS Sistema de Garantías",
    },
    twitter: {
        card: "summary_large_image",
        title: "Sistema de Gestión de Garantías - MCQS",
        description: "Gestión eficiente de cartas fianza y obras.",
    },
    robots: {
        index: true,
        follow: true,
    }
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="es">
            <head>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
            </head>
            <body className={montserrat.className}>
                <Providers>
                    {children}
                </Providers>
                <Script src="https://cdn.jsdelivr.net/npm/chart.js" strategy="beforeInteractive" />
            </body>
        </html>
    );
}
