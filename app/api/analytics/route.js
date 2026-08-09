export async function GET() {
  try {
    const response = await fetch(
      "http://192.168.0.102:8000/analytics/"
    );

    const data = await response.json();

    return Response.json(data, {
      status: response.status,
    });
  } catch (error) {
    console.error("Analytics backend error:", error);

    return Response.json(
      {
        detail: "Could not connect to FastAPI",
        error: error.message,
      },
      { status: 500 }
    );
  }
}