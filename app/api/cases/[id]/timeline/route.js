import { NextResponse } from "next/server";

export async function GET(request, { params }) {
  try {
    const { id } = await params;

    const backendUrl =
      `https://ai-investigation-copilot.onrender.com/cases/${id}/timeline`;

    console.log("TIMELINE ID:", id);
    console.log("TIMELINE URL:", backendUrl);

    const response = await fetch(backendUrl, {
      cache: "no-store",
    });

    const data = await response.json();

    console.log("TIMELINE STATUS:", response.status);
    console.log("TIMELINE DATA:", data);

    return NextResponse.json({
      debug: true,
      id,
      backendUrl,
      backendStatus: response.status,
      data,
    });

  } catch (error) {
    console.error("TIMELINE API ERROR:", error);

    return NextResponse.json(
      {
        debug: true,
        error: error.message,
      },
      {
        status: 500,
      }
    );
  }
}