import { NextResponse } from "next/server";

export async function GET(request, { params }) {
  try {
    const { id } = await params;

    const response = await fetch(
      `http://192.168.0.102:8000/cases/${id}`
    );

    const data = await response.json();

    return NextResponse.json(data, {
      status: response.status,
    });

  } catch (error) {
    console.error("CASE API ERROR:", error);

    return NextResponse.json(
      {
        detail: "Failed to connect to backend",
      },
      {
        status: 500,
      }
    );
  }
}