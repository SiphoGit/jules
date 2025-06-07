import Link from 'next/link';

const Navbar = () => {
  return (
    <nav className="bg-gray-800 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link href="/" className="text-xl font-bold">AssetManagerAI</Link>
        <div className="space-x-4">
          <Link href="/dashboard" className="hover:text-gray-300">Dashboard</Link>
          {/* Add other links here as pages are created, e.g., Login/Logout */}
          <Link href="/login" className="hover:text-gray-300">Login</Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
