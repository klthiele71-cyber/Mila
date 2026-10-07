# Mila V10 – External Gateway Rules

V10 prepares the technical boundary for real external services.

## Rules
- External providers must be explicitly allowlisted.
- Only HTTPS endpoints and explicitly allowlisted hosts are accepted.
- Credentials are supplied by a separate credential provider and are never stored in model/provider objects.
- The external gateway does not authorize user-sensitive actions.
- The AI model remains untrusted: model output may propose work but cannot grant permission.
- Missing credentials, non-HTTPS endpoints, or non-allowlisted providers/hosts are blocked.
- A real provider can be connected later by supplying a transport and credential source.
- This version does not require API credits and does not make a live external request during tests.
