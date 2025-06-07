import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css'; // Imports Tailwind
import Layout from '@/components/Layout'; // Import the new Layout

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'AI Asset Management',
  description: 'Manage your assets intelligently',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Layout>
          {children}
        </Layout>
      </body>
    </html>
  );
}
