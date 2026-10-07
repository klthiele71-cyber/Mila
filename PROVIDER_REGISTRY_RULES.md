# V11 Provider Registry Rules
- Provider selection is explicit and allowlisted.
- Disabled providers cannot be selected.
- Credentials are referenced by name only; secrets are never stored in model objects.
- Registration never grants permission to perform sensitive actions.
- A provider adapter is untrusted external infrastructure and cannot alter Mila security decisions.
