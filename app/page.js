import Link from "next/link";

export default function Login() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-black">

      <div className="bg-white shadow-xl rounded-xl p-10 w-96">

        <h1 className="text-3xl font-bold text-center text-blue-900 mb-8">
          🔍 AI Investigation Copilot
        </h1>

        <input
          type="text"
          placeholder="Officer ID"
          className="w-full border border-gray-300 p-3 rounded-lg mb-4 text-black placeholder:text-gray-500"
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full border border-gray-300 p-3 rounded-lg mb-6 text-black placeholder:text-gray-500"
          />

        <Link href="/dashboard">
          <button className="w-full bg-blue-800 hover:bg-blue-900 text-white py-3 rounded-lg">
            Login
          </button>
        </Link>

      </div>

    </main>
  );
}