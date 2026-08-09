import { NextResponse } from "next/server";

export async function POST(request) {
  try {
    const body = await request.json();

    const response = await fetch(
      "https://ai-investigation-copilot.onrender.com/cases/",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      }
    );

    const data = await response.json();

    return NextResponse.json(data, {
      status: response.status,
    });
  } catch (error) {
    console.error("CREATE CASE API ERROR:", error);

    return NextResponse.json(
      {
        detail: "Failed to connect to backend",
        error: error.message,
      },
      { status: 500 }
    );
  }
}

export async function GET(request) {
  try {
    const { searchParams } = new URL(request.url);
    const id = searchParams.get("id");

    if (!id) {
      return NextResponse.json(
        { detail: "Case ID is required" },
        { status: 400 }
      );
    }

    const response = await fetch(
      `https://ai-investigation-copilot.onrender.com/cases/${encodeURIComponent(id)}`
    );

    const data = await response.json();

    return NextResponse.json(data, {
      status: response.status,
    });
  } catch (error) {
    console.error("GET CASE API ERROR:", error);

    return NextResponse.json(
      {
        detail: "Failed to connect to backend",
        error: error.message,
      },
      { status: 500 }
    );
  }
}