import Link from "next/link";

export default function Dashboard() {
  return (
    <main className="min-h-screen bg-slate-100 p-10">

      <h1 className="text-4xl font-bold text-blue-900">
        Welcome Officer Ravi 👮
      </h1>

      <div className="grid grid-cols-3 gap-6 mt-8">

        <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
          <h2 className="text-blue-800 font-semibold">Active Cases</h2>
          <p className="text-4xl font-bold mt-3 text-red-600">24</p>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
          <h2 className="text-blue-800 font-semibold">Documents</h2>
          <p className="text-4xl font-bold mt-3 text-red-600">136</p>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
          <h2 className="text-blue-800 font-semibold">Alerts</h2>
          <p className="text-4xl font-bold mt-3 text-red-600">5</p>
        </div>

      </div>

      <Link href="/create-case">
        <button className="mt-10 bg-blue-800 text-white px-6 py-3 rounded-lg hover:bg-blue-900">
          ➕ Create New Case
        </button>
      </Link>

    </main>
  );
}