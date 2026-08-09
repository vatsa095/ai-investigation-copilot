export async function GET(request) {
  try {
    const { searchParams } = new URL(request.url);
    const suspect = searchParams.get("suspect");

    if (!suspect) {
      return Response.json(
        { detail: "Suspect name is required" },
        { status: 400 }
      );
    }

    const response = await fetch(`https://ai-investigation-copilot.onrender.com/search/?query=${encodeURIComponent(query)}`)

    const data = await response.json();

    return Response.json(data, {
      status: response.status,
    });
  } catch (error) {
    console.error("AI backend error:", error);

    return Response.json(
      {
        detail: "Could not connect to AI backend",
        error: error.message,
      },
      { status: 500 }
    );
  }
}