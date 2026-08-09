    "use client";

    import { useState, useEffect } from "react";
    import InvestigationGraph from "../components/InvestigationGraph";

    export default function SearchPage() {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);

    const [aiReport, setAiReport] = useState(null);
    const [aiLoading, setAiLoading] = useState(false);
    const [aiSuspect, setAiSuspect] = useState("");
    useEffect(() => {
    if (aiReport) {
        setTimeout(() => {
        document.getElementById("ai-report")?.scrollIntoView({
            behavior: "smooth",
            block: "start",
        });
        }, 100);
    }
    }, [aiReport]);

    const handleSearch = async (e) => {
        e.preventDefault();

        if (!query.trim()) {
        return;
        }

        setLoading(true);
        setResults(null);
        setAiReport(null);

        try {
        const response = await fetch(
            `/api/search?query=${encodeURIComponent(query)}`
        );

        const data = await response.json();

        if (!response.ok) {
            console.error("Search error:", data);
            alert("Search failed");
            return;
        }

        console.log("Search results:", data);
        setResults(data);
        } catch (error) {
        console.error("SEARCH ERROR:", error);
        alert("Failed to connect to backend");
        } finally {
        setLoading(false);
        }
    };

    const analyzeWithAI = async (suspectName) => {
    console.log("🔥 AI BUTTON CLICKED:", suspectName);

    setAiLoading(true);
    setAiReport(null);
    setAiSuspect(suspectName);

    try {
        const url = `/api/ai?suspect=${encodeURIComponent(suspectName)}`;

        console.log("🤖 CALLING:", url);

        const response = await fetch(url);

        console.log("📡 STATUS:", response.status);

        const data = await response.json();

        console.log("📦 AI DATA:", data);

        if (!response.ok) {
        throw new Error(data.detail || "AI analysis failed");
        }

        setAiReport(data);

        console.log("✅ REPORT SET");

    } catch (error) {
        console.error("❌ AI ERROR:", error);
        alert("AI analysis failed: " + error.message);

    } finally {
        setAiLoading(false);
    }
    };

    return (
        <main className="min-h-screen bg-gray-100 p-8">
        <div className="max-w-6xl mx-auto">

            {/* Header */}
            <div className="mb-8">
            <h1 className="text-4xl font-bold text-blue-900">
                Investigation Search 🔍
            </h1>

            <p className="text-gray-600 mt-2">
                Search suspects, phone numbers, vehicles and cases.
            </p>
            </div>

            {/* Search Box */}
            <form
            onSubmit={handleSearch}
            className="bg-white p-6 rounded-xl shadow-sm flex gap-4"
            >
            <input
                type="text"
                placeholder="Enter suspect, phone, vehicle or case..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="flex-1 border border-gray-300 p-3 rounded-lg text-black"
            />

            <button
                type="submit"
                disabled={loading}
                className="bg-blue-800 text-white px-7 py-3 rounded-lg hover:bg-blue-900 disabled:opacity-50"
            >
                {loading ? "Searching..." : "Search"}
            </button>
            </form>

            {/* Results */}
            {results && (
            <div className="mt-8 space-y-6">

                {/* Persons */}
                {results.persons?.length > 0 && (
                <section className="bg-white rounded-xl shadow-sm p-6">

                    <h2 className="text-2xl font-bold text-blue-900 mb-5">
                    👤 Persons
                    </h2>

                    {results.persons.map((person) => (
                    <div
                        key={person.id}
                        className="border rounded-lg p-4 text-black"
                    >
                        <p className="text-xl font-bold">
                        {person.full_name}
                        </p>

                        {person.alias && (
                        <p className="text-gray-600">
                            Alias: {person.alias}
                        </p>
                        )}

                        <button
                        onClick={() =>
                            analyzeWithAI(person.full_name)
                        }
                        className="mt-4 bg-purple-700 text-white px-5 py-2 rounded-lg hover:bg-purple-800"
                        >
                        🤖 Analyze with AI
                        </button>
                    </div>
                    ))}

                </section>
                )}

                {/* Connected Cases */}
                {results.person_cases?.length > 0 && (
                <section className="bg-white rounded-xl shadow-sm p-6">

                    <h2 className="text-2xl font-bold text-blue-900 mb-5">
                    🔗 Connected Cases
                    </h2>

                    {results.person_cases.map((item, index) => (
                    <div
                        key={index}
                        className="border rounded-lg p-5 mb-4 text-black"
                    >

                        <div className="flex justify-between items-center">

                        <div>
                            <p className="text-xl font-bold text-blue-800">
                            {item.case_number}
                            </p>

                            <p className="text-gray-600">
                            Suspect: {item.person}
                            </p>

                            <p className="text-gray-600">
                            Role: {item.role}
                            </p>
                        </div>

                        <span className="bg-red-100 text-red-700 px-3 py-1 rounded-full text-sm font-semibold">
                            {item.crime_type}
                        </span>

                        </div>

                        <div className="grid grid-cols-2 gap-4 mt-5">

                        <p>
                            <strong>Location:</strong>{" "}
                            {item.location}
                        </p>

                        <p>
                            <strong>Incident Date:</strong>{" "}
                            {item.incident_date}
                        </p>

                        </div>

                        <p className="mt-4">
                        <strong>Summary:</strong>{" "}
                        {item.summary}
                        </p>

                        <button
                        onClick={() =>
                            analyzeWithAI(item.person)
                        }
                        className="mt-5 bg-purple-700 text-white px-5 py-2 rounded-lg hover:bg-purple-800"
                        >
                        🤖 Analyze {item.person} with AI
                        </button>

                    </div>
                    ))}

                </section>
                )}

                {/* Connected Phones */}
                {results.phone_cases?.length > 0 && (
                <section className="bg-white rounded-xl shadow-sm p-6">

                    <h2 className="text-2xl font-bold text-blue-900 mb-5">
                    📱 Connected Phone Numbers
                    </h2>

                    {results.phone_cases.map((phone, index) => (
                    <div
                        key={index}
                        className="border rounded-lg p-4 mb-3 text-black"
                    >

                        <p className="text-lg font-bold">
                        {phone.phone_number}
                        </p>

                        <p className="text-gray-600">
                        Associated Person: {phone.person}
                        </p>

                        <p className="text-gray-600">
                        Case: {phone.case_number}
                        </p>

                        <p className="text-gray-600">
                        Crime: {phone.crime_type}
                        </p>

                    </div>
                    ))}

                </section>
                )}

                {/* Connected Vehicles */}
                {results.vehicle_cases?.length > 0 && (
                <section className="bg-white rounded-xl shadow-sm p-6">

                    <h2 className="text-2xl font-bold text-blue-900 mb-5">
                    🚗 Connected Vehicles
                    </h2>

                    {results.vehicle_cases.map((vehicle, index) => (
                    <div
                        key={index}
                        className="border rounded-lg p-4 mb-3 text-black"
                    >

                        <p className="text-lg font-bold">
                        {vehicle.vehicle_number}
                        </p>

                        <p className="text-gray-600">
                        Associated Person: {vehicle.person}
                        </p>

                        <p className="text-gray-600">
                        Case: {vehicle.case_number}
                        </p>

                        <p className="text-gray-600">
                        Crime: {vehicle.crime_type}
                        </p>

                    </div>
                    ))}

                </section>
                )}

                {/* Direct Phones */}
                {results.phones?.length > 0 && (
                <section className="bg-white rounded-xl shadow-sm p-6">

                    <h2 className="text-2xl font-bold text-blue-900 mb-5">
                    📱 Phone Numbers
                    </h2>

                    {results.phones.map((phone) => (
                    <div
                        key={phone.id}
                        className="border-b py-3 text-black"
                    >
                        {phone.phone_number}
                    </div>
                    ))}

                </section>
                )}

                {/* Direct Vehicles */}
                {results.vehicles?.length > 0 && (
                <section className="bg-white rounded-xl shadow-sm p-6">

                    <h2 className="text-2xl font-bold text-blue-900 mb-5">
                    🚗 Vehicles
                    </h2>

                    {results.vehicles.map((vehicle) => (
                    <div
                        key={vehicle.id}
                        className="border-b py-3 text-black"
                    >
                        {vehicle.vehicle_number}
                    </div>
                    ))}

                </section>
                )}

                {/* Direct Cases */}
                {results.cases.map((caseItem) => (
    <div
        key={caseItem.id}
        onClick={() => {
        window.location.href = `/case/${caseItem.id}`;
        }}
        className="border rounded-lg p-5 mb-3 text-black cursor-pointer hover:bg-blue-50 hover:border-blue-400 transition"
    >
        <div className="flex justify-between items-center">

        <div>
            <p className="font-bold text-blue-800 text-xl">
            {caseItem.case_number}
            </p>

            <p className="mt-1">
            {caseItem.crime_type} — {caseItem.location}
            </p>

            <p className="text-gray-500 mt-1">
            Incident Date: {caseItem.incident_date}
            </p>
        </div>

        <span className="text-blue-700 font-semibold">
            View Case →
        </span>

        </div>
    </div>
    ))}

                {/* AI Investigation Report */}
    {aiReport && (
    <section
        id="ai-report"
        className="bg-white rounded-xl shadow-lg p-6 border-2 border-purple-200"
    >

        <div className="flex justify-between items-center mb-5">

        <h2 className="text-2xl font-bold text-purple-800">
            🤖 AI Investigation Report
        </h2>

        <span className="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-sm">
            AI Analysis
        </span>

        </div>

        <div className="bg-gray-900 text-green-300 rounded-lg p-6 whitespace-pre-wrap font-mono text-sm">
        {aiReport.report}
        </div>

    </section>
    )}
    {/* Next Best Actions */}
{aiReport?.assessment?.recommendations?.length > 0 && (
  <section className="bg-white rounded-xl shadow-lg p-6 border-2 border-orange-200">

    <h2 className="text-2xl font-bold text-orange-800 mb-2">
      🎯 Next-Best Investigation Actions
    </h2>

    <p className="text-gray-600 mb-5">
      AI-generated recommendations based on patterns found across
      the connected cases.
    </p>

    <div className="space-y-4">

      {aiReport.assessment.recommendations.map(
        (recommendation, index) => {

          const isHigh =
            recommendation.priority === "HIGH";

          return (
            <div
              key={index}
              className={`border rounded-xl p-5 ${
                isHigh
                  ? "border-red-200 bg-red-50"
                  : "border-orange-200 bg-orange-50"
              }`}
            >

              <div className="flex items-start gap-4">

                <div
                  className={`px-3 py-1 rounded-full text-xs font-bold ${
                    isHigh
                      ? "bg-red-100 text-red-700"
                      : "bg-orange-100 text-orange-700"
                  }`}
                >
                  {recommendation.priority}
                </div>

                <div className="flex-1">

                  <p className="font-semibold text-gray-900">
                    {index + 1}. {recommendation.action}
                  </p>

                  <p className="text-sm text-gray-600 mt-2">
                    <strong>Why:</strong>{" "}
                    {recommendation.reason}
                  </p>

                </div>

              </div>

            </div>
          );
        }
      )}

    </div>

  </section>
)}

    {/* Investigation Network */}
    {aiReport?.analysis && (
    <section className="bg-white rounded-xl shadow-lg p-6 border-2 border-blue-200">

        <h2 className="text-2xl font-bold text-blue-900 mb-2">
        🔗 Investigation Network
        </h2>

        <p className="text-gray-600 mb-5">
        Visual relationship map showing connections between the
        suspect, cases, phones, vehicles and locations.
        </p>

        <InvestigationGraph
  analysis={aiReport.analysis}
  assessment={aiReport.assessment}
/>
        {/* Case Connection Analysis */}
{aiReport?.assessment?.connections?.length > 0 && (
  <section className="bg-white rounded-xl shadow-lg p-6 border-2 border-blue-200 mt-6">

    <h2 className="text-2xl font-bold text-blue-900 mb-2">
      🔗 Case Connection Analysis
    </h2>

    <p className="text-gray-600 mb-5">
      Cases are ranked according to shared investigative identifiers
      and observed similarities.
    </p>

    <div className="space-y-3">

      {aiReport.assessment.connections.map(
        (connection, index) => (

          <div
            key={index}
            className="border rounded-xl p-4 flex items-center justify-between"
          >

            <div>

              <p className="font-bold text-blue-800">
                CASE{String(connection.case_id).padStart(3, "0")}
              </p>

              <p className="text-gray-600">
                {connection.crime_type}
                {" — "}
                {connection.location}
              </p>

              <div className="flex flex-wrap gap-2 mt-2">

                {connection.reasons.map(
                  (reason, reasonIndex) => (
                    <span
                      key={reasonIndex}
                      className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs"
                    >
                      {reason}
                    </span>
                  )
                )}

              </div>

            </div>

            <div className="text-right">

              <span
                className={`px-3 py-1 rounded-full text-sm font-bold ${
                  connection.strength === "HIGH"
                    ? "bg-red-100 text-red-700"
                    : connection.strength === "MEDIUM"
                    ? "bg-orange-100 text-orange-700"
                    : "bg-gray-100 text-gray-700"
                }`}
              >
                {connection.strength}
              </span>

              <p className="text-2xl font-bold text-gray-800 mt-1">
                {connection.score}
              </p>

              <p className="text-xs text-gray-500">
                connection score
              </p>

            </div>

          </div>

        )
      )}

    </div>

  </section>
)}

    </section>
    )}

                {/* AI Loading */}
                {aiLoading && (
                <section className="bg-purple-50 border border-purple-200 rounded-xl p-6">
                    <p className="text-purple-800 font-semibold">
                    🤖 AI is analyzing {aiSuspect}...
                    </p>

                    <p className="text-gray-600 mt-2">
                    Checking linked cases, phone numbers, vehicles,
                    crime types and locations.
                    </p>
                </section>
                )}

                {/* No Results */}
                {results.persons?.length === 0 &&
                results.person_cases?.length === 0 &&
                results.phones?.length === 0 &&
                results.phone_cases?.length === 0 &&
                results.vehicles?.length === 0 &&
                results.vehicle_cases?.length === 0 &&
                results.cases?.length === 0 && (

                <div className="bg-white p-8 rounded-xl shadow-sm text-center">
                    <p className="text-gray-600 text-lg">
                    No matching records found.
                    </p>
                </div>
                )}

            </div>
            )}

        </div>
        </main>
    );
    }