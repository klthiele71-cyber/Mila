/**
 * Mila – Cloudflare Worker
 * Verbindung zwischen Mila-iPhone-Prototyp und OpenAI
 *
 * WICHTIG:
 * Der OpenAI-Schlüssel steht NICHT hier im Code.
 * Er wird in Cloudflare als Secret mit dem Namen OPENAI_API_KEY hinterlegt.
 */

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Content-Type": "application/json; charset=utf-8",
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: CORS_HEADERS,
  });
}

export default {
  async fetch(request, env) {
    // CORS-Vorprüfung
    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: CORS_HEADERS,
      });
    }

    // Nur POST-Anfragen für Mila
    if (request.method !== "POST") {
      return json({
        ok: true,
        service: "Mila API",
        message: "Mila Worker ist erreichbar.",
      });
    }

    // API-Key muss als Cloudflare Secret vorhanden sein
    if (!env.OPENAI_API_KEY) {
      return json(
        {
          error: "OPENAI_API_KEY ist in Cloudflare nicht als Secret hinterlegt.",
        },
        500
      );
    }

    let body;

    try {
      body = await request.json();
    } catch {
      return json({ error: "Ungültige JSON-Anfrage." }, 400);
    }

    const message =
      typeof body?.message === "string"
        ? body.message.trim()
        : typeof body?.input === "string"
          ? body.input.trim()
          : "";

    if (!message) {
      return json({ error: "Keine Nachricht übergeben." }, 400);
    }

    try {
      const openaiResponse = await fetch(
        "https://api.openai.com/v1/responses",
        {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${env.OPENAI_API_KEY}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            model: "gpt-5",
            instructions:
              "Du bist Mila, eine freundliche, aufmerksame und hilfreiche KI-Begleiterin. Antworte auf Deutsch, natürlich und verständlich. Behandle Klaus respektvoll und freundlich. Antworte direkt auf seine Frage und erfinde keine Tatsachen.",
            input: message,
          }),
        }
      );

      const data = await openaiResponse.json();

      if (!openaiResponse.ok) {
        return json(
          {
            error:
              data?.error?.message ||
              "Die OpenAI-Anfrage konnte nicht verarbeitet werden.",
          },
          openaiResponse.status
        );
      }

      const reply =
        typeof data?.output_text === "string" ? data.output_text.trim() : "";

      if (!reply) {
        return json(
          {
            error: "OpenAI hat keine Textantwort zurückgegeben.",
          },
          502
        );
      }

      return json({ reply });
    } catch (error) {
      return json(
        {
          error:
            error?.message ||
            "Fehler bei der Verbindung mit der OpenAI-Schnittstelle.",
        },
        500
      );
    }
  },
};
