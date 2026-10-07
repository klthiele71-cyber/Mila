# Instance Isolation Rules

- The personal Mila instance is identified as `master`.
- New Mila instances are isolated by default.
- A child/shared instance cannot access master or master-owned data.
- Creating/transferring an instance does not copy master memory, sessions, credentials, approvals, or private data.
- Master may later establish a one-way, explicitly authorized link to a shared instance.
- A master-to-shared link never grants reverse access.
- Links are revocable and auditable.
- Instance isolation is enforced outside the model; prompts or model output cannot override it.
