"use client";

import { useState } from "react";
import Link from "next/link";

export default function CreateCase() {
  const [caseName, setCaseName] = useState("");

console.log(caseName);


  return (
    <main className="min-h-screen bg-slate-100 flex justify-center items-center">

      <div className="bg-white p-10 rounded-xl shadow-xl w-[500px]">

        <h1 className="text-3xl font-bold text-blue-900 mb-6">
          Create New Case
        </h1>

        <input
  className="w-full border border-gray-300 p-3 rounded-lg mb-4 text-black"
  placeholder="Case Name"
  value={caseName}
  onChange={(e) => setCaseName(e.target.value)}
/>

        <input
          className="w-full border border-gray-300 p-3 rounded-lg mb-4 text-black"
          placeholder="Officer Name"
        />

        <textarea
          className="w-full border border-gray-300 p-3 rounded-lg mb-4 text-black"
          rows="4"
          placeholder="Case Description"
        />

        <select className="w-full border border-gray-300 p-3 rounded-lg mb-6 text-black">
          <option>Low</option>
          <option>Medium</option>
          <option>High</option>
        </select>

        <Link href={`/case?name=${encodeURIComponent(caseName)}`}>
          <button className="w-full bg-blue-800 text-white py-3 rounded-lg hover:bg-blue-900">
            Create Case
          </button>
        </Link>

      </div>

    </main>
  );
}
