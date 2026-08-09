export async function POST(request) {
  try {
    const body = await request.json();

    const response = await fetch("http://127.0.0.1:8000/cases/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    const data = await response.json();

    return Response.json(data, {
      status: response.status,
    });

  } catch (error) {
    console.error("FastAPI connection error:", error);

    return Response.json(
      {
        detail: "Could not connect to FastAPI",
        error: error.message,
      },
      { status: 500 }
    );
  }
}