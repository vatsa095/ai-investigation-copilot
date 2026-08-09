export async function GET(request) {
  try {
    const { searchParams } = new URL(request.url);

    const query = searchParams.get("query");

    if (!query) {
      return Response.json(
        { detail: "Search query is required" },
        { status: 400 }
      );
    }

    const response = await fetch(
      `http://192.168.0.102:8000/search/?query=${encodeURIComponent(
        query
      )}`
    );

    const data = await response.json();

    return Response.json(data, {
      status: response.status,
    });
  } catch (error) {
    console.error("Search backend error:", error);

    return Response.json(
      {
        detail: "Could not connect to FastAPI",
        error: error.message,
      },
      { status: 500 }
    );
  }
}