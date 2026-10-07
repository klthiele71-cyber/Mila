# Mila V33 – Live API Preflight

V33 adds the final preflight check before a live OpenAI request.
Missing credentials block readiness. A successful preflight does not itself execute a request or authorize Mila actions.
The first actual live request is intentionally not performed in development because it requires configured API access and may incur usage charges.
