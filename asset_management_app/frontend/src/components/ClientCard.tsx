import Link from 'next/link';
import { Client } from '@/services/api'; // Assuming api.ts is in src/services

interface ClientCardProps {
  client: Client;
}

const ClientCard: React.FC<ClientCardProps> = ({ client }) => {
  return (
    <div className="bg-white shadow-lg rounded-lg p-6 mb-4 hover:shadow-xl transition-shadow duration-300 ease-in-out">
      <h3 className="text-xl font-semibold text-indigo-700 mb-2">{client.first_name} {client.last_name}</h3>
      <p className="text-gray-600 text-sm mb-1">Email: {client.email}</p>
      <p className="text-gray-600 text-sm mb-3">Risk Profile: <span className="font-medium text-gray-800">{client.risk_profile}</span></p>
      <div className="flex justify-between items-center">
        <Link href={`/clients/${client.id}/portfolio`} className="text-sm text-indigo-600 hover:text-indigo-800 font-medium">
          View Portfolio
        </Link>
        <Link href={`/clients/${client.id}/recommendations`} className="text-sm text-green-600 hover:text-green-800 font-medium">
          Get Recommendations
        </Link>
      </div>
    </div>
  );
};

export default ClientCard;
