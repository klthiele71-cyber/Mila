# V12 Request Policy Rules
- Every outbound request is bounded by timeout, payload size, and retry limits.
- Default retry count is one: no uncontrolled retry loops.
- Policy validation occurs before transport.
- The policy cannot grant authorization for sensitive actions.
