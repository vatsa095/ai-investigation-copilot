"use client";

import {
  ReactFlow,
  Background,
  Controls,
  useNodesState,
  useEdgesState,
} from "reactflow";

import "reactflow/dist/style.css";


function createGraph(analysis, assessment) {

  const nodes = [];
  const edges = [];

  const suspectId = "suspect";

  // --------------------------------
  // SUSPECT
  // --------------------------------

  nodes.push({
    id: suspectId,

    position: {
      x: 500,
      y: 300,
    },

    data: {
      label: `👤 ${analysis.suspect_name}`,
    },

    style: {
      background: "#7c3aed",
      color: "white",
      padding: 16,
      borderRadius: 14,
      fontWeight: "bold",
      border: "2px solid #5b21b6",
      fontSize: "16px",
    },
  });


  // --------------------------------
  // PHONE
  // --------------------------------

  (analysis.phone_numbers || []).forEach(
    (phone, index) => {

      const id = `phone-${index}`;

      nodes.push({
        id,

        position: {
          x: 100,
          y: 120 + index * 120,
        },

        data: {
          label: `📱 ${phone}`,
        },

        style: {
          background: "#dbeafe",
          color: "#1e3a8a",
          padding: 12,
          borderRadius: 10,
          border: "2px solid #3b82f6",
        },
      });

      edges.push({
        id: `edge-phone-${index}`,
        source: suspectId,
        target: id,

        style: {
          stroke: "#3b82f6",
          strokeWidth: 2,
        },
      });

    }
  );


  // --------------------------------
  // VEHICLE
  // --------------------------------

  (analysis.vehicle_numbers || []).forEach(
    (vehicle, index) => {

      const id = `vehicle-${index}`;

      nodes.push({
        id,

        position: {
          x: 900,
          y: 120 + index * 120,
        },

        data: {
          label: `🚗 ${vehicle}`,
        },

        style: {
          background: "#dcfce7",
          color: "#166534",
          padding: 12,
          borderRadius: 10,
          border: "2px solid #22c55e",
        },
      });

      edges.push({
        id: `edge-vehicle-${index}`,
        source: suspectId,
        target: id,

        style: {
          stroke: "#22c55e",
          strokeWidth: 2,
        },
      });

    }
  );


  // --------------------------------
  // LOCATION
  // --------------------------------

  (analysis.locations || []).forEach(
    (location, index) => {

      const id = `location-${index}`;

      nodes.push({
        id,

        position: {
          x: 500,
          y: 80 + index * 100,
        },

        data: {
          label: `📍 ${location}`,
        },

        style: {
          background: "#fef3c7",
          color: "#92400e",
          padding: 12,
          borderRadius: 10,
          border: "2px solid #f59e0b",
        },
      });

      edges.push({
        id: `edge-location-${index}`,
        source: suspectId,
        target: id,

        style: {
          stroke: "#f59e0b",
          strokeWidth: 2,
        },
      });

    }
  );


  // --------------------------------
  // CONNECTED CASES
  // --------------------------------

  const connections =
    assessment?.connections || [];

  connections.forEach(
    (connection, index) => {

      const id = `case-${index}`;

      const strength =
        connection.strength || "LOW";

      let background = "#f3f4f6";
      let border = "#9ca3af";
      let color = "#374151";

      if (strength === "HIGH") {
        background = "#fee2e2";
        border = "#ef4444";
        color = "#991b1b";
      }

      if (strength === "MEDIUM") {
        background = "#ffedd5";
        border = "#f97316";
        color = "#9a3412";
      }

      const reasons =
        connection.reasons || [];

      const reasonText =
        reasons.join(" • ");

      nodes.push({

        id,

        position: {
          x: 180 + (index % 4) * 270,
          y: 500 + Math.floor(index / 4) * 150,
        },

        data: {

          label: (
            <div>

              <div className="font-bold">
                📁 {connection.case_number}
              </div>

              <div className="text-xs mt-1">
                {connection.crime_type}
              </div>

              <div className="text-xs mt-1">
                Score: {connection.score}
              </div>

              <div className="text-xs font-bold mt-1">
                {strength}
              </div>

              {reasonText && (
                <div className="text-[10px] mt-2 opacity-80">
                  {reasonText}
                </div>
              )}

            </div>
          ),
        },

        style: {
          background,
          color,
          padding: 12,
          borderRadius: 12,
          border: `2px solid ${border}`,
          width: 220,
          fontWeight: "bold",
        },

      });


      // Case connection edge

      edges.push({

        id: `edge-case-${index}`,

        source: suspectId,

        target: id,

        style: {
          stroke:
            strength === "HIGH"
              ? "#ef4444"
              : strength === "MEDIUM"
              ? "#f97316"
              : "#9ca3af",

          strokeWidth:
            strength === "HIGH"
              ? 3
              : 2,
        },

        label: `${connection.score}`,

      });

    }
  );


  return {
    nodes,
    edges,
  };
}


export default function InvestigationGraph({
  analysis,
  assessment,
}) {

  const graph =
    createGraph(
      analysis,
      assessment
    );

  const [
    nodes,
    setNodes,
    onNodesChange,
  ] = useNodesState(
    graph.nodes
  );

  const [
    edges,
    setEdges,
    onEdgesChange,
  ] = useEdgesState(
    graph.edges
  );


  return (

    <div
      style={{
        width: "100%",
        height: "700px",
      }}

      className="
        rounded-xl
        overflow-hidden
        border
        border-purple-200
        bg-gray-50
      "
    >
      <div className="absolute top-3 left-3 z-10 bg-white/95 rounded-lg shadow-md px-4 py-3 text-xs">
  <p className="font-bold text-gray-800 mb-2">
    Connection Legend
  </p>

  <div className="flex gap-4 flex-wrap">
    <span className="text-red-600 font-semibold">
      🔴 HIGH
    </span>

    <span className="text-orange-600 font-semibold">
      🟠 MEDIUM
    </span>

    <span className="text-blue-600">
      📱 Phone
    </span>

    <span className="text-green-600">
      🚗 Vehicle
    </span>

    <span className="text-yellow-700">
      📍 Location
    </span>
  </div>
</div>

      <ReactFlow
  nodes={nodes}
  edges={edges}
  onNodesChange={onNodesChange}
  onEdgesChange={onEdgesChange}
  fitView
  fitViewOptions={{
    padding: 0.2,
  }}
  proOptions={{
    hideAttribution: true,
  }}
>
  <Background />
  <Controls />
</ReactFlow>
    </div>

  );
}