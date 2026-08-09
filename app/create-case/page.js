"use client";

import { useState } from "react";

export default function CreateCase() {
  const [formData, setFormData] = useState({
    crime_type: "",
    suspect_name: "",
    phone_number: "",
    vehicle_number: "",
    location: "",
    incident_date: "",
    evidence: "",
    summary: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

const handleSubmit = async (e) => {
  e.preventDefault();

  console.log("Sending case:", formData);

  try {
 const response = await fetch("/api/cases", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(formData),
});
    console.log("Response status:", response.status);

    const data = await response.json();

    console.log("Response:", data);

    if (!response.ok) {
      console.error("Backend error:", data);
      alert("Failed to create case");
      return;
    }

    console.log("Case Created:", data);
    alert("Case " + data.case_number + " created successfully!");

  } catch (error) {
    console.error("FETCH ERROR:", error);
    alert("Failed to connect to backend");
  }
};

  return (
    <main className="min-h-screen bg-gray-100 flex items-center justify-center p-6">
      <div className="bg-white p-10 rounded-xl shadow-xl w-[500px]">

        <h1 className="text-3xl font-bold text-blue-900 mb-6">
          Create New Case
        </h1>

        <form onSubmit={handleSubmit}>

          {/* Crime Type */}
          <select
            name="crime_type"
            value={formData.crime_type}
            onChange={handleChange}
            className="w-full border border-gray-300 p-3 rounded-lg mb-4 text-black"
            required
          >
            <option value="">Select Crime Type</option>
            <option value="Murder">Murder</option>
            <option value="Burglary">Burglary</option>
            <option value="Theft">Theft</option>
            <option value="Robbery">Robbery</option>
            <option value="Kidnapping">Kidnapping</option>
            <option value="Cybercrime">Cybercrime</option>
            <option value="Drug Trafficking">Drug Trafficking</option>
            <option value="Financial Fraud">Financial Fraud</option>
            <option value="Vehicle Theft">Vehicle Theft</option>
            <option value="Assault">Assault</option>
            <option value="Missing Person">Missing Person</option>
          </select>

          {/* Suspect Name */}
          <input
            name="suspect_name"
            className="w-full border border-gray-300 p-3 rounded-lg mb-4 text-black"
            placeholder="Suspect Name"
            value={formData.suspect_name}
            onChange={handleChange}
            required
          />

          {/* Phone Number */}
          <input
            name="phone_number"
            className="w-full border border-gray-300 p-3 rounded-lg mb-4 text-black"
            placeholder="Phone Number"
            value={formData.phone_number}
            onChange={handleChange}
          />

          {/* Vehicle Number */}
          <input
            name="vehicle_number"
            className="w-full border border-gray-300 p-3 rounded-lg mb-4 text-black"
            placeholder="Vehicle Number"
            value={formData.vehicle_number}
            onChange={handleChange}
          />

          {/* Location */}
          <input
            name="location"
            className="w-full border border-gray-300 p-3 rounded-lg mb-4 text-black"
            placeholder="Location"
            value={formData.location}
            onChange={handleChange}
            required
          />

          {/* Incident Date */}
          <input
            type="date"
            name="incident_date"
            value={formData.incident_date}
            onChange={handleChange}
            className="w-full border border-gray-300 p-3 rounded-lg mb-4 text-black"
            required
          />

          {/* Evidence */}
          <input
            name="evidence"
            className="w-full border border-gray-300 p-3 rounded-lg mb-4 text-black"
            placeholder="Evidence"
            value={formData.evidence}
            onChange={handleChange}
            required
          />

          {/* Case Summary */}
          <textarea
            name="summary"
            rows="4"
            className="w-full border border-gray-300 p-3 rounded-lg mb-6 text-black"
            placeholder="Case Summary"
            value={formData.summary}
            onChange={handleChange}
            required
          />

          <button
            type="submit"
            className="w-full bg-blue-800 text-white py-3 rounded-lg hover:bg-blue-900"
          >
            Save Case
          </button>

        </form>

      </div>
    </main>
  );
}