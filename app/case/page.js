"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import dynamic from "next/dynamic";

const MovementMap = dynamic(
  () => import("../components/MovementMap"),
  {
    ssr: false,
  }
);

export default function CasePage() {

  const searchParams = useSearchParams();

  const [fileName, setFileName] = useState("");
  const [timeline, setTimeline] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // ------------------------------------------------
  // GET CASE ID FROM URL
  //
  // Example:
  // /case?case_id=101
  // ------------------------------------------------

  const caseId =
    searchParams.get("case_id");


  // ------------------------------------------------
  // LOAD TIMELINE
  // ------------------------------------------------

  useEffect(() => {

    async function loadTimeline() {

      // No case selected yet
      if (!caseId) {

        setLoading(false);
        setTimeline([]);

        return;

      }

      try {

        setLoading(true);
        setError("");

        const response = await fetch(
          `/api/cases/${caseId}/timeline`
        );

        if (!response.ok) {

          throw new Error(
            "Failed to load movement timeline"
          );

        }

        const data =
          await response.json();

        setTimeline(data);

      } catch (err) {

        console.error(err);

        setError(
          "Could not load movement timeline."
        );

      } finally {

        setLoading(false);

      }

    }

    loadTimeline();

  }, [caseId]);


  return (

    <main className="min-h-screen bg-slate-100 p-10">

      {/* ================================================= */}
      {/* PAGE TITLE */}
      {/* ================================================= */}

      <h1 className="text-4xl font-bold text-blue-900">
        Case Investigation
      </h1>


      {/* ================================================= */}
      {/* CURRENT CASE */}
      {/* ================================================= */}

      <div className="bg-white rounded-xl shadow-lg mt-8 p-6">

        <h2 className="text-xl font-semibold text-black">

          {caseId
            ? `Case ${caseId}`
            : "No Case Selected"}

        </h2>

        {!caseId && (

          <p className="text-gray-600 mt-2">

            Open a case to view its investigation
            and movement timeline.

          </p>

        )}

      </div>


      {/* ================================================= */}
      {/* FIR UPLOAD */}
      {/* ================================================= */}

      <div className="bg-white rounded-xl shadow-lg mt-8 p-8">

        <h2 className="text-2xl font-semibold mb-4 text-black">
          Upload FIR
        </h2>

        <input
          type="file"
          id="firUpload"
          className="hidden"
          onChange={(e) => {

            if (
              e.target.files &&
              e.target.files.length > 0
            ) {

              setFileName(
                e.target.files[0].name
              );

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


      {/* ================================================= */}
      {/* MOVEMENT MAP */}
      {/* ================================================= */}

      {caseId && (

        <div className="bg-white rounded-xl shadow-lg mt-8 p-8">

          <div className="flex items-center justify-between mb-5">

            <div>

              <h2 className="text-2xl font-semibold text-black">

                🗺️ Post-Incident Movement

              </h2>

              <p className="text-gray-600 mt-1">

                Documented locations associated with Case{" "}
                {caseId}

              </p>

            </div>

          </div>


          {/* LOADING */}

          {loading && (

            <div className="h-[500px] flex items-center justify-center text-gray-600">

              Loading movement data...

            </div>

          )}


          {/* ERROR */}

          {!loading && error && (

            <div className="h-[200px] flex items-center justify-center text-red-600">

              {error}

            </div>

          )}


          {/* MAP */}

          {!loading &&
            !error &&
            timeline.length > 0 && (

              <MovementMap
                timeline={timeline}
              />

            )}


          {/* NO EVENTS */}

          {!loading &&
            !error &&
            timeline.length === 0 && (

              <div className="h-[200px] flex items-center justify-center text-gray-500">

                No documented movement events
                are available for this case.

              </div>

            )}

        </div>

      )}


      {/* ================================================= */}
      {/* TIMELINE LIST */}
      {/* ================================================= */}

      {!loading &&
        timeline.length > 0 && (

          <div className="bg-white rounded-xl shadow-lg mt-8 p-8">

            <h2 className="text-2xl font-semibold text-black mb-6">

              Investigation Timeline

            </h2>


            <div className="space-y-4">

              {timeline.map((item) => (

                <div
                  key={item.id}
                  className="border-l-4 border-blue-700 pl-5 py-3"
                >

                  <div className="flex items-center gap-3">

                    <span className="font-semibold text-blue-800 uppercase">

                      {item.event_type}

                    </span>

                    <span className="text-gray-500">

                      {new Date(
                        item.event_time
                      ).toLocaleString()}

                    </span>

                  </div>


                  <p className="text-black mt-1">

                    {item.event}

                  </p>


                  {item.location && (

                    <p className="text-gray-600 mt-1">

                      📍 {item.location}

                    </p>

                  )}


                  {item.source && (

                    <p className="text-gray-500 text-sm mt-1">

                      Source: {item.source}

                    </p>

                  )}

                </div>

              ))}

            </div>

          </div>

        )}

    </main>

  );

}