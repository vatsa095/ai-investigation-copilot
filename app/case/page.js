"use client";

import { useState } from "react";

export default function CasePage() {

  const [fileName, setFileName] = useState("");

  return (
    <main className="min-h-screen bg-slate-100 p-10">

      <h1 className="text-4xl font-bold text-blue-900">
        Case Investigation
      </h1>

      <div className="bg-white rounded-xl shadow-lg mt-8 p-8">

        <h2 className="text-2xl font-semibold mb-4 text-black">
          Upload FIR
        </h2>

        <input
          type="file"
          id="firUpload"
          className="hidden"
          onChange={(e) => {
            if (e.target.files.length > 0) {
              setFileName(e.target.files[0].name);
            }
          }}
        />

        <label
          htmlFor="firUpload"
          className="bg-blue-800 text-white px-6 py-3 rounded-lg cursor-pointer hover:bg-blue-900 inline-block"
        >
          Choose FIR
        </label>

        {fileName && (
          <p className="mt-4 text-green-700 font-medium">
            ✅ Selected File: {fileName}
          </p>
        )}

      </div>

    </main>
  );
}