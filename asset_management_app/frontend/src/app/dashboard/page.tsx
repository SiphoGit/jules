"use client";

import React, { useEffect, useState } from 'react';
import ClientCard from '@/components/ClientCard';
import { getClients, Client } from '@/services/api'; // Assuming api.ts is in src/services
import Link from 'next/link';

const DashboardPage = () => {
  const [clients, setClients] = useState<Client[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchClients = async () => {
      try {
        setLoading(true);
        const data = await getClients();
        setClients(data);
        setError(null);
      } catch (err) {
        console.error("Failed to fetch clients:", err);
        setError(err instanceof Error ? err.message : "An unknown error occurred.");
      } finally {
        setLoading(false);
      }
    };
    fetchClients();
  }, []);

  if (loading) return <p className="text-center text-gray-600 py-10">Loading clients...</p>;
  if (error) return <p className="text-center text-red-500 py-10">Error loading clients: {error}. Ensure backend is running.</p>;

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Client Dashboard</h1>
        {/* Placeholder for Add Client button or functionality */}
        {/* <Link href="/clients/new" className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
          Add New Client
        </Link> */}
      </div>

      {clients.length === 0 ? (
        <p className="text-center text-gray-500">No clients found. (Ensure backend is running and has data).</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {clients.map(client => (
            <ClientCard key={client.id} client={client} />
          ))}
        </div>
      )}
    </div>
  );
};

export default DashboardPage;
