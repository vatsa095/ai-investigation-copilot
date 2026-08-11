import { NextResponse } from "next/server";

const BACKEND_URL =
  process.env.BACKEND_URL ||
  "https://ai-investigation-copilot.onrender.com";

export async function GET(request) {
  try {
    const { searchParams } = new URL(request.url);

    const suspectName = searchParams.get("suspect");

    if (!suspectName) {
      return NextResponse.json(
        {
          error: "Suspect name is required"
        },
        {
          status: 400
        }
      );
    }

    const backendUrl =
      `${BACKEND_URL}/ai/investigate/` +
      encodeURIComponent(suspectName);

    const response = await fetch(
      backendUrl,
      {
        method: "GET",
        headers: {
          Accept: "application/json"
        },
        cache: "no-store"
      }
    );

    const text = await response.text();

    let data;

    try {
      data = JSON.parse(text);
    } catch {
      return NextResponse.json(
        {
          error: "Backend returned invalid JSON",
          backendResponse: text
        },
        {
          status: 502
        }
      );
    }

    if (!response.ok) {
      return NextResponse.json(
        data,
        {
          status: response.status
        }
      );
    }

    return NextResponse.json(data);
  } catch (error) {
    console.error(
      "AI backend connection error:",
      error
    );

    return NextResponse.json(
      {
        error: "Could not connect to AI backend",
        details: error.message
      },
      {
        status: 502
      }
    );
  }
}