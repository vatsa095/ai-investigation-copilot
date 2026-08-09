"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";

export default function CaseDetailsPage() {
  const params = useParams();
  const router = useRouter();

  const [caseData, setCaseData] = useState(null);
  const [loading, setLoading] = useState(true);

useEffect(() => {
  const loadCase = async () => {
    try {
      const response = await fetch(`/api/cases?id=${params.id}`);

      if (!response.ok) {
        throw new Error("Failed to load case");
      }

      const data = await response.json();
      setCaseData(data);
    } catch (error) {
      console.error("CASE ERROR:", error);
    } finally {
      setLoading(false);
    }
  };

  if (params.id) {
    loadCase();
  }
}, [params.id]);

  if (loading) {
    return (
      <main className="min-h-screen bg-gray-100 p-8">
        <p className="text-blue-900 text-lg">
          Loading case...
        </p>
      </main>
    );
  }

  if (!caseData) {
    return (
      <main className="min-h-screen bg-gray-100 p-8">
        <p className="text-red-600 text-lg">
          Case not found.
        </p>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto">

        {/* Header */}
        <div className="flex justify-between items-center mb-8">

          <div>
            <p className="text-gray-500 mb-1">
              Investigation Case
            </p>

            <h1 className="text-4xl font-bold text-blue-900">
              {caseData.case_number}
            </h1>

            <p className="text-xl text-gray-700 mt-2">
              {caseData.crime_type}
            </p>
          </div>

          <button
            onClick={() => router.back()}
            className="bg-gray-700 text-white px-5 py-3 rounded-lg hover:bg-gray-800"
          >
            ← Back
          </button>

        </div>

        {/* Basic Information */}
        <section className="bg-white rounded-xl shadow-sm p-6 mb-6">

          <h2 className="text-2xl font-bold text-blue-900 mb-6">
            📋 Case Information
          </h2>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">

            <div>
              <p className="text-gray-500">Crime Type</p>
              <p className="font-semibold text-black mt-1">
                {caseData.crime_type}
              </p>
            </div>

            <div>
              <p className="text-gray-500">Status</p>
              <span className="inline-block mt-1 bg-green-100 text-green-700 px-3 py-1 rounded-full font-semibold">
                {caseData.status}
              </span>
            </div>

            <div>
              <p className="text-gray-500">Location</p>
              <p className="font-semibold text-black mt-1">
                📍 {caseData.location}
              </p>
            </div>

            <div>
              <p className="text-gray-500">Incident Date</p>
              <p className="font-semibold text-black mt-1">
                📅 {caseData.incident_date}
              </p>
            </div>

          </div>

        </section>

        {/* Summary */}
        <section className="bg-white rounded-xl shadow-sm p-6 mb-6">

          <h2 className="text-2xl font-bold text-blue-900 mb-4">
            📝 Case Summary
          </h2>

          <p className="text-gray-700 leading-7">
            {caseData.summary || "No summary available."}
          </p>

        </section>

        {/* Suspect */}
        {caseData.persons?.length > 0 && (
          <section className="bg-white rounded-xl shadow-sm p-6 mb-6">

            <h2 className="text-2xl font-bold text-blue-900 mb-5">
              👤 Associated Persons
            </h2>

            {caseData.persons.map((person) => (
              <div
                key={person.id}
                className="border rounded-lg p-5 mb-3"
              >

                <p className="text-xl font-bold text-black">
                  {person.full_name}
                </p>

                <p className="text-gray-600 mt-1">
                  Role: {person.role}
                </p>

                {person.phone && (
                  <p className="text-gray-600 mt-2">
                    📱 {person.phone}
                  </p>
                )}

                {person.vehicle && (
                  <p className="text-gray-600 mt-1">
                    🚗 {person.vehicle}
                  </p>
                )}

              </div>
            ))}

          </section>
        )}

        {/* Evidence */}
        {caseData.evidence?.length > 0 && (
          <section className="bg-white rounded-xl shadow-sm p-6 mb-6">

            <h2 className="text-2xl font-bold text-blue-900 mb-5">
              🧾 Evidence
            </h2>

            {caseData.evidence.map((item, index) => (
              <div
                key={item.id || index}
                className="border rounded-lg p-5 mb-3"
              >

                <p className="font-bold text-black">
                  {item.evidence_type}
                </p>

                <p className="text-gray-600 mt-2">
                  {item.description}
                </p>

              </div>
            ))}

          </section>
        )}

        {/* Investigation Notes */}
        {caseData.investigations?.length > 0 && (
          <section className="bg-white rounded-xl shadow-sm p-6 mb-6">

            <h2 className="text-2xl font-bold text-blue-900 mb-5">
              📝 Investigation Notes
            </h2>

            {caseData.investigations.map((note, index) => (
              <div
                key={note.id || index}
                className="border rounded-lg p-5 mb-3"
              >

                <p className="font-semibold text-black">
                  Officer: {note.officer_name}
                </p>

                <p className="text-gray-700 mt-2">
                  {note.notes}
                </p>

                {note.next_step && (
                  <p className="text-blue-700 mt-3">
                    <strong>Next Step:</strong>{" "}
                    {note.next_step}
                  </p>
                )}

              </div>
            ))}

          </section>
        )}

      </div>
    </main>
  );
}