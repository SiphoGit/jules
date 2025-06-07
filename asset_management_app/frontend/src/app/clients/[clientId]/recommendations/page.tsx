"use client";

import React, { useEffect, useState }
from 'react';
import { useParams, useRouter } from 'next/navigation';
import { getClientById, getRecommendations, Client, RecommendedAsset, MarketTrend, RecommendationRequest } from '@/services/api';
import AssetTable from '@/components/AssetTable'; // Re-use AssetTable
import Link from 'next/link';

const ClientRecommendationsPage = () => {
  const router = useRouter();
  const params = useParams();
  const clientId = params?.clientId ? parseInt(params.clientId as string) : null;

  const [client, setClient] = useState<Client | null>(null);
  const [recommendations, setRecommendations] = useState<RecommendedAsset[]>([]);
  const [marketTrend, setMarketTrend] = useState<MarketTrend>(MarketTrend.NEUTRAL);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [loadingRecs, setLoadingRecs] = useState(false);

  useEffect(() => {
    if (!clientId) {
      setError("Client ID not found in URL.");
      setLoading(false);
      return;
    }
    const fetchClientData = async () => {
      try {
        setLoading(true);
        const clientData = await getClientById(clientId);
        setClient(clientData);
        // Optionally fetch initial recommendations here or wait for user action
        await fetchRecommendations(clientData.risk_profile, marketTrend, clientId); // Pass client ID
      } catch (err) {
        console.error("Failed to fetch client data:", err);
        setError(err instanceof Error ? err.message : "An unknown error occurred.");
      } finally {
        setLoading(false);
      }
    };
    fetchClientData();
  }, [clientId]); // Initial fetch depends only on clientId

  const fetchRecommendations = async (profile: Client['risk_profile'], trend: MarketTrend, currentClientId: number) => {
    if (!currentClientId) return;
    try {
      setLoadingRecs(true);
      setError(null);
      const recRequest: RecommendationRequest = { market_trend: trend };
      const data = await getRecommendations(currentClientId, recRequest);
      setRecommendations(data);
    } catch (err) {
      console.error("Failed to fetch recommendations:", err);
      setError(err instanceof Error ? err.message : "An unknown error occurred while fetching recommendations.");
      setRecommendations([]); // Clear previous recommendations on error
    } finally {
      setLoadingRecs(false);
    }
  };

  const handleFetchRecommendations = () => {
      if (client && clientId) {
          fetchRecommendations(client.risk_profile, marketTrend, clientId);
      }
  };

  if (loading) return <p className="text-center text-gray-600 py-10">Loading client information...</p>;
  // Separate loading state for recommendations so client info still shows
  // if (error && !client) return <p className="text-center text-red-500 py-10">Error: {error}</p>; // Only show fatal error if client fails
  if (!client) return <p className="text-center text-gray-500 py-10">Client data not found.</p>;


  return (
    <div>
      <button onClick={() => router.back()} className="mb-6 bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold py-2 px-4 rounded inline-flex items-center">
        &larr; Back
      </button>
      <h1 className="text-3xl font-bold text-gray-800 mb-2">
        Asset Recommendations for {client.first_name} {client.last_name}
      </h1>
      <p className="text-lg text-gray-600 mb-4">Risk Profile: <span className="font-medium">{client.risk_profile}</span></p>

      <div className="mb-6 p-4 bg-gray-50 rounded-lg shadow">
        <label htmlFor="marketTrend" className="block text-sm font-medium text-gray-700 mb-1">Select Market Trend:</label>
        <div className="flex items-center space-x-4">
          <select
            id="marketTrend"
            value={marketTrend}
            onChange={(e) => setMarketTrend(e.target.value as MarketTrend)}
            className="block w-full max-w-xs px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          >
            {Object.values(MarketTrend).map(trend => (
              <option key={trend} value={trend}>{trend.charAt(0).toUpperCase() + trend.slice(1)}</option>
            ))}
          </select>
          <button
            onClick={handleFetchRecommendations}
            disabled={loadingRecs}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:bg-blue-300"
          >
            {loadingRecs ? 'Fetching...' : 'Get New Recommendations'}
          </button>
        </div>
      </div>

      {error && <p className="text-center text-red-500 py-5">Error: {error}</p>}

      {loadingRecs && <p className="text-center text-gray-600 py-5">Loading recommendations...</p>}
      {!loadingRecs && recommendations.length > 0 && (
        <AssetTable assets={recommendations} title="Recommended Assets" />
      )}
      {!loadingRecs && recommendations.length === 0 && !error && (
         <p className="text-center text-gray-500 py-5">No recommendations available for the selected criteria, or initial load pending user action.</p>
      )}
    </div>
  );
};

export default ClientRecommendationsPage;
