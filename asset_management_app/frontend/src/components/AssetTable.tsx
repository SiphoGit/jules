import { RecommendedAsset } from '@/services/api'; // Using RecommendedAsset as it includes all Asset fields

interface AssetTableProps {
  assets: RecommendedAsset[]; // Could also be PortfolioDetailsResponse.assets_details
  title?: string;
}

const AssetTable: React.FC<AssetTableProps> = ({ assets, title = "Assets" }) => {
  if (!assets || assets.length === 0) {
    return <p className="text-gray-600">No assets to display.</p>;
  }

  return (
    <div className="my-6">
      <h3 className="text-2xl font-semibold text-gray-700 mb-4">{title}</h3>
      <div className="overflow-x-auto bg-white shadow-md rounded-lg">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ticker</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
              <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
              {/* Optional: Add quantity and value if this table is for portfolio view with those details */}
              {assets[0]?.suitability_score !== undefined && (
                 <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Suitability</th>
              )}
               {assets[0]?.rationale !== undefined && (
                 <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Rationale</th>
              )}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {assets.map((asset) => (
              <tr key={asset.id || asset.ticker_symbol} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{asset.name}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{asset.ticker_symbol}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{asset.asset_type}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-500">${asset.current_price.toFixed(2)}</td>
                {asset.suitability_score !== undefined && (
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-500">{asset.suitability_score.toFixed(2)}</td>
                )}
                {asset.rationale && (
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 max-w-xs truncate" title={asset.rationale}>{asset.rationale}</td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AssetTable;
