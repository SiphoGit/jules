import React from 'react';
import Navbar from './Navbar';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow container mx-auto p-4">
        {children}
      </main>
      <footer className="bg-gray-200 text-center p-4 text-sm text-gray-600">
        © 2023 AI Asset Management App
      </footer>
    </div>
  );
};

export default Layout;
