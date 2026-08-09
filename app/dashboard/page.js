"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
const CHART_COLORS = [
  "#2563eb",
  "#ef4444",
  "#22c55e",
  "#f59e0b",
  "#8b5cf6",
  "#06b6d4",
  "#ec4899",
  "#84cc16",
  "#f97316",
  "#14b8a6",
  "#6366f1",
  "#e11d48",
];

export default function Dashboard() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadAnalytics = async () => {
    try {
      const response = await fetch("/api/analytics");

      if (!response.ok) {
        throw new Error("Failed to load analytics");
      }

      const data = await response.json();
      setAnalytics(data);
    } catch (error) {
      console.error("Analytics error:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAnalytics();

    // Refresh dashboard every 10 seconds
    const interval = setInterval(loadAnalytics, 10000);

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <main className="min-h-screen bg-gray-100 p-8">
        <h1 className="text-3xl font-bold text-blue-900">
          Loading Dashboard...
        </h1>
      </main>
    );
  }

  if (!analytics) {
    return (
      <main className="min-h-screen bg-gray-100 p-8">
        <h1 className="text-3xl font-bold text-red-700">
          Failed to load dashboard
        </h1>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-7xl mx-auto">

        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-4xl font-bold text-blue-900">
              Welcome Officer 👮🫡
            </h1>

            <p className="text-gray-600 mt-2">
              AI Investigation Command Center
            </p>
          </div>

          <div className="flex gap-3">

            <Link href="/search">
              <button className="bg-gray-800 text-white px-5 py-3 rounded-lg hover:bg-gray-900">
                🔍 Search Investigation
              </button>
            </Link>

            <Link href="/create-case">
              <button className="bg-blue-800 text-white px-5 py-3 rounded-lg hover:bg-blue-900">
                ➕ Create Case
              </button>
            </Link>

          </div>
        </div>


        {/* Statistics */}
        <div className="grid grid-cols-4 gap-6 mt-8">

          <div className="bg-white border border-blue-200 rounded-xl p-6 shadow-sm">
            <h2 className="text-gray-600 font-semibold">
              Total Cases
            </h2>

            <p className="text-4xl font-bold mt-3 text-blue-800">
              {analytics.total_cases}
            </p>
          </div>


          <div className="bg-white border border-red-200 rounded-xl p-6 shadow-sm">
            <h2 className="text-gray-600 font-semibold">
              Active Cases
            </h2>

            <p className="text-4xl font-bold mt-3 text-red-600">
              {analytics.open_cases}
            </p>
          </div>


          <div className="bg-white border border-green-200 rounded-xl p-6 shadow-sm">
            <h2 className="text-gray-600 font-semibold">
              Persons
            </h2>

            <p className="text-4xl font-bold mt-3 text-green-600">
              {analytics.total_persons}
            </p>
          </div>


          <div className="bg-white border border-purple-200 rounded-xl p-6 shadow-sm">
            <h2 className="text-gray-600 font-semibold">
              Evidence
            </h2>

            <p className="text-4xl font-bold mt-3 text-purple-600">
              {analytics.total_evidence}
            </p>
          </div>

        </div>


       {/* Analytics */}

<div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">

  {/* Crime Analysis */}

  <div className="bg-white rounded-xl p-6 shadow-sm">

    <h2 className="text-2xl font-bold text-blue-900 mb-2">
      📊 Crime Analysis
    </h2>

    <p className="text-sm text-gray-500 mb-4">
      Top 5 crime categories
    </p>

    {analytics.crime_distribution.length === 0 ? (

      <p className="text-gray-500">
        No crime data available.
      </p>

    ) : (

      <>
        {/* PIE CHART */}

        <div className="h-[300px]">

          <ResponsiveContainer
            width="100%"
            height="100%"
          >

            <PieChart>

              <Pie
                data={analytics.crime_distribution}
                dataKey="count"
                nameKey="crime_type"
                cx="50%"
                cy="50%"
                outerRadius={105}
                innerRadius={55}
                paddingAngle={2}
              >

                {analytics.crime_distribution.map(
                  (crime, index) => (

                    <Cell
                      key={crime.crime_type}
                      fill={
                        CHART_COLORS[
                          index % CHART_COLORS.length
                        ]
                      }
                    />

                  )
                )}

              </Pie>

              <Tooltip
                formatter={(value, name) => [
                  `${value} cases`,
                  name,
                ]}
              />

            </PieChart>

          </ResponsiveContainer>

        </div>


        {/* TOP 5 */}

        <div className="mt-4 space-y-2">

          {[
            ...analytics.crime_distribution
          ]
            .sort((a, b) => b.count - a.count)
            .slice(0, 5)
            .map((crime, index) => {

              const total =
                analytics.crime_distribution.reduce(
                  (sum, item) =>
                    sum + item.count,
                  0
                );

              const percentage =
                total > 0
                  ? (
                      (crime.count / total) *
                      100
                    ).toFixed(1)
                  : "0.0";

              return (

                <div
                  key={crime.crime_type}
                  className="flex items-center justify-between px-3 py-2 rounded-lg bg-gray-50"
                >

                  <div className="flex items-center gap-3">

                    <span
                      className="w-3 h-3 rounded-full"
                      style={{
                        backgroundColor:
                          CHART_COLORS[
                            index %
                              CHART_COLORS.length
                          ],
                      }}
                    />

                    <span className="font-medium text-gray-700">
                      {crime.crime_type}
                    </span>

                  </div>

                  <span className="font-semibold text-blue-900">
                    {percentage}%
                  </span>

                </div>

              );
            })}

        </div>

      </>

    )}

  </div>


  {/* Location Analysis */}

  <div className="bg-white rounded-xl p-6 shadow-sm">

    <h2 className="text-2xl font-bold text-blue-900 mb-2">
      📍 Location Analysis
    </h2>

    <p className="text-sm text-gray-500 mb-4">
      Top 5 locations
    </p>

    {analytics.location_distribution.length === 0 ? (

      <p className="text-gray-500">
        No location data available.
      </p>

    ) : (

      <>
        {/* PIE CHART */}

        <div className="h-[300px]">

          <ResponsiveContainer
            width="100%"
            height="100%"
          >

            <PieChart>

              <Pie
                data={analytics.location_distribution}
                dataKey="count"
                nameKey="location"
                cx="50%"
                cy="50%"
                outerRadius={105}
                innerRadius={55}
                paddingAngle={2}
              >

                {analytics.location_distribution.map(
                  (location, index) => (

                    <Cell
                      key={location.location}
                      fill={
                        CHART_COLORS[
                          index %
                            CHART_COLORS.length
                        ]
                      }
                    />

                  )
                )}

              </Pie>

              <Tooltip
                formatter={(value, name) => [
                  `${value} cases`,
                  name,
                ]}
              />

            </PieChart>

          </ResponsiveContainer>

        </div>


        {/* TOP 5 */}

        <div className="mt-4 space-y-2">

          {[
            ...analytics.location_distribution
          ]
            .sort((a, b) => b.count - a.count)
            .slice(0, 5)
            .map((location, index) => {

              const total =
                analytics.location_distribution.reduce(
                  (sum, item) =>
                    sum + item.count,
                  0
                );

              const percentage =
                total > 0
                  ? (
                      (location.count / total) *
                      100
                    ).toFixed(1)
                  : "0.0";

              return (

                <div
                  key={location.location}
                  className="flex items-center justify-between px-3 py-2 rounded-lg bg-gray-50"
                >

                  <div className="flex items-center gap-3">

                    <span
                      className="w-3 h-3 rounded-full"
                      style={{
                        backgroundColor:
                          CHART_COLORS[
                            index %
                              CHART_COLORS.length
                          ],
                      }}
                    />

                    <span className="font-medium text-gray-700">
                      {location.location}
                    </span>

                  </div>

                  <span className="font-semibold text-blue-900">
                    {percentage}%
                  </span>

                </div>

              );
            })}

        </div>

      </>

    )}

  </div>

</div>


        {/* Recent Cases */}
        <div className="bg-white rounded-xl p-6 shadow-sm mt-8">

          <h2 className="text-2xl font-bold text-blue-900 mb-6">
            🕒 Recent Cases
          </h2>

          <div className="overflow-x-auto">

            <table className="w-full">

              <thead>
                <tr className="border-b text-left">

                  <th className="py-3 text-gray-600">
                    Case
                  </th>

                  <th className="py-3 text-gray-600">
                    Crime
                  </th>

                  <th className="py-3 text-gray-600">
                    Location
                  </th>

                  <th className="py-3 text-gray-600">
                    Date
                  </th>

                  <th className="py-3 text-gray-600">
                    Status
                  </th>

                </tr>
              </thead>

              <tbody>

                {analytics.recent_cases.map((caseItem) => (

                  <tr
                    key={caseItem.id}
                    className="border-b hover:bg-gray-50"
                  >

                    <td className="py-4 font-bold text-blue-800">
                      {caseItem.case_number}
                    </td>

                    <td className="py-4 text-gray-700">
                      {caseItem.crime_type}
                    </td>

                    <td className="py-4 text-gray-700">
                      {caseItem.location}
                    </td>

                    <td className="py-4 text-gray-700">
                      {caseItem.incident_date}
                    </td>

                    <td className="py-4">

                      <span
                        className={`px-3 py-1 rounded-full text-sm font-semibold ${
                          caseItem.status === "Open"
                            ? "bg-red-100 text-red-700"
                            : "bg-green-100 text-green-700"
                        }`}
                      >
                        {caseItem.status}
                      </span>

                    </td>

                  </tr>

                ))}

              </tbody>

            </table>

          </div>

        </div>


        {/* AI Insight */}
        <div className="bg-blue-900 text-white rounded-xl p-6 mt-8 shadow-lg">

          <h2 className="text-2xl font-bold mb-3">
            🤖 AI Investigation Insight
          </h2>

          <p className="text-blue-100">
            The dashboard is monitoring{" "}
            <strong className="text-white">
              {analytics.total_cases}
            </strong>{" "}
            cases across{" "}
            <strong className="text-white">
              {analytics.location_distribution.length}
            </strong>{" "}
            locations. Crime pattern analysis and
            investigation recommendations will appear here
            once AI analysis is connected.
          </p>

        </div>

      </div>
    </main>
    
  );
}