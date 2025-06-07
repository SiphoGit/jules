"use client";

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation'; // App router hooks
import { getClientById, getClientPortfolio, Client, PortfolioDetailsResponse, RecommendedAsset } from '@/services/api';
import AssetTable from '@/components/AssetTable'; // Re-use AssetTable
import Link from 'next/link';

const ClientPortfolioPage = () => {
  const router = useRouter();
  const params = useParams(); // For accessing [clientId]
  const clientId = params?.clientId ? parseInt(params.clientId as string) : null;

  const [client, setClient] = useState<Client | null>(null);
  const [portfolio, setPortfolio] = useState<PortfolioDetailsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!clientId) {
      setError("Client ID not found in URL.");
      setLoading(false);
      return;
    }

    const fetchData = async () => {
      try {
        setLoading(true);
        const clientData = await getClientById(clientId);
        setClient(clientData);
        const portfolioData = await getClientPortfolio(clientId);
        setPortfolio(portfolioData);
        setError(null);
      } catch (err) {
        console.error("Failed to fetch data:", err);
        setError(err instanceof Error ? err.message : "An unknown error occurred.");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [clientId]);

  if (loading) return <p className="text-center text-gray-600 py-10">Loading portfolio details...</p>;
  if (error) return <p className="text-center text-red-500 py-10">Error: {error}</p>;
  if (!client || !portfolio) return <p className="text-center text-gray-500 py-10">Client or portfolio data not found.</p>;

  // The assets_details in PortfolioDetailsResponse is already List[RecommendedAsset]
  // which matches what AssetTable expects.
  const assetsForTable: RecommendedAsset[] = portfolio.assets_details.map(ad => ({
      ...ad, // Spread existing fields from RecommendedAsset (name, ticker, type, price, score, rationale)
      // If quantity or value specific to portfolio context were needed here for AssetTable,
      // and PortfolioDetailsResponse.assets_details didn't have them (e.g. if it was just List[Asset]),
      // we would need to map them from portfolio.assets (which has PortfolioAsset with quantity)
      // However, current PortfolioDetailsResponse in main.py uses RecommendedAsset which doesn't have quantity.
      // The backend's crud.get_portfolio_details provides 'value' and 'quantity' but this is not used
      // by PortfolioDetailsResponse.assets_details currently.
      // For now, AssetTable will display what's in RecommendedAsset.
  }));


  return (
    <div>
      <button onClick={() => router.back()} className="mb-6 bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold py-2 px-4 rounded inline-flex items-center">
        &larr; Back to Dashboard
      </button>
      <h1 className="text-3xl font-bold text-gray-800 mb-2">
        Portfolio for {client.first_name} {client.last_name}
      </h1>
      <p className="text-lg text-gray-600 mb-1">Portfolio Name: <span className="font-medium">{portfolio.name}</span></p>
      <p className="text-lg text-gray-600 mb-6">Total Value: <span className="font-semibold text-green-600">${portfolio.total_value.toFixed(2)}</span></p>

      <AssetTable assets={assetsForTable} title="Current Holdings" />

      {/* Placeholder for Add/Remove Asset functionality */}
      {/* <div className="mt-8">
        <h3 className="text-xl font-semibold text-gray-700 mb-3">Manage Assets</h3>
        <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Add New Asset to Portfolio (Not Implemented)
        </button>
      </div> */}
    </div>
  );
};

export default ClientPortfolioPage;
