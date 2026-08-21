"use client";

import { useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

export default function MovementMap({ timeline = [] }) {

  const mapContainerRef = useRef(null);
  const mapRef = useRef(null);

  useEffect(() => {

    // Prevent creating the map more than once
    if (
      mapRef.current ||
      !mapContainerRef.current
    ) {
      return;
    }

    // ----------------------------------------------------
    // CREATE MAP
    // ----------------------------------------------------

    const map = L.map(
      mapContainerRef.current
    ).setView(
      [12.9716, 77.5946],
      11
    );

    mapRef.current = map;

    // ----------------------------------------------------
    // OPENSTREETMAP REAL MAP
    // ----------------------------------------------------

    L.tileLayer(
      "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',

        maxZoom: 19
      }
    ).addTo(map);


    // ----------------------------------------------------
    // MARKER COLORS
    // ----------------------------------------------------

    const colors = {

      crime: "#dc2626",

      cctv: "#2563eb",

      vehicle: "#16a34a",

      phone: "#9333ea",

      witness: "#f97316",

      other: "#64748b"

    };


    // ----------------------------------------------------
    // CREATE MARKER ICON
    // ----------------------------------------------------

    function createIcon(type) {

      const color =
        colors[type?.toLowerCase()] ||
        colors.other;

      return L.divIcon({

        className: "",

        html: `
          <div style="
            width: 22px;
            height: 22px;
            background: ${color};
            border: 3px solid white;
            border-radius: 50%;
            box-shadow: 0 2px 6px rgba(0,0,0,0.4);
          "></div>
        `,

        iconSize: [22, 22],

        iconAnchor: [11, 11]

      });

    }


    // ----------------------------------------------------
    // VALID EVENTS
    // ----------------------------------------------------

    const validEvents = timeline.filter(
      (item) => {

        const lat =
          Number(item.latitude);

        const lng =
          Number(item.longitude);

        return (
          Number.isFinite(lat) &&
          Number.isFinite(lng)
        );

      }
    );


    // ----------------------------------------------------
    // MARKERS
    // ----------------------------------------------------

    const points = [];

    validEvents.forEach(
      (item, index) => {

        const lat =
          Number(item.latitude);

        const lng =
          Number(item.longitude);

        points.push([
          lat,
          lng
        ]);


        const marker =
          L.marker(
            [lat, lng],
            {
              icon: createIcon(
                item.event_type
              )
            }
          ).addTo(map);


        // ------------------------------------------------
        // POPUP
        // ------------------------------------------------

        const eventType =
          item.event_type ||
          "other";

        const event =
          item.event ||
          "No description";

        const location =
          item.location ||
          "Unknown location";

        const source =
          item.source ||
          "Unknown source";

        const confidence =
          item.confidence ||
          "MEDIUM";

        const eventTime =
          item.event_time
            ? new Date(
                item.event_time
              ).toLocaleString()
            : "Unknown time";


        marker.bindPopup(`
          <div style="
            min-width: 220px;
            font-family: Arial, sans-serif;
          ">

            <h3 style="
              margin: 0 0 8px 0;
              font-size: 16px;
              font-weight: bold;
            ">
              ${eventType.toUpperCase()}
            </h3>

            <p style="
              margin: 4px 0;
            ">
              <b>Time:</b>
              ${eventTime}
            </p>

            <p style="
              margin: 4px 0;
            ">
              <b>Location:</b>
              ${location}
            </p>

            <p style="
              margin: 4px 0;
            ">
              <b>Evidence:</b>
              ${event}
            </p>

            <p style="
              margin: 4px 0;
            ">
              <b>Source:</b>
              ${source}
            </p>

            <p style="
              margin: 4px 0;
            ">
              <b>Confidence:</b>
              ${confidence}
            </p>

            <p style="margin: 4px 0;">
  <b>Case:</b>
  ${item.case_reference || item.case_id || "Unknown"}
</p>

          </div>
        `);

      }
    );


    // ----------------------------------------------------
    // CHRONOLOGICAL MOVEMENT LINE
    // ----------------------------------------------------

    if (points.length >= 2) {

      L.polyline(
        points,
        {
          color: "#334155",
          weight: 4,
          opacity: 0.75,
          dashArray: "8, 8"
        }
      ).addTo(map);

    }


    // ----------------------------------------------------
    // FIT MAP TO EVENTS
    // ----------------------------------------------------

    if (points.length > 0) {

      const bounds =
        L.latLngBounds(points);

      map.fitBounds(
        bounds,
        {
          padding: [40, 40]
        }
      );

    }


    // ----------------------------------------------------
    // CLEANUP
    // ----------------------------------------------------

    return () => {

      map.remove();

      mapRef.current = null;

    };

  }, [timeline]);


  return (

    <div>

      {/* MAP */}

      <div
        ref={mapContainerRef}
        className="w-full h-[500px] rounded-xl overflow-hidden border border-slate-300"
      />


      {/* LEGEND */}

      <div className="flex flex-wrap gap-5 mt-4 text-sm">

        <Legend
          color="#dc2626"
          label="Crime"
        />

        <Legend
          color="#2563eb"
          label="CCTV"
        />

        <Legend
          color="#16a34a"
          label="Vehicle"
        />

        <Legend
          color="#9333ea"
          label="Phone"
        />

        <Legend
          color="#f97316"
          label="Witness"
        />

        <Legend
          color="#64748b"
          label="Other"
        />

      </div>

    </div>

  );

}


// ========================================================
// LEGEND ITEM
// ========================================================

function Legend({
  color,
  label
}) {

  return (

    <div className="flex items-center gap-2">

      <span
        style={{
          width: 12,
          height: 12,
          background: color,
          borderRadius: "50%",
          display: "inline-block"
        }}
      />

      <span className="text-gray-700">
        {label}
      </span>

    </div>

  );

}