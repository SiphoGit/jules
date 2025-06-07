import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="text-center">
      <h1 className="text-4xl font-bold my-10 text-gray-800">Welcome to the AI Asset Management Platform</h1>
      <p className="text-lg text-gray-600 mb-8">
        Manage your financial assets with cutting-edge AI insights.
      </p>
      <div>
        <Link href="/dashboard" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg text-lg mr-4">
          Go to Dashboard
        </Link>
        <Link href="/login" className="bg-green-500 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg text-lg">
          Login
        </Link>
      </div>
    </div>
  );
}
