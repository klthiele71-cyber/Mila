# V33 Master Isolation Rules

The personal Mila instance is called `Master`.

1. Master is the user's personal instance.
2. Shared/family instances are separate instances with separate identity and state.
3. Shared instances cannot access Master in any direction without a supported authorization path; the architecture provides no reverse shared->Master link.
4. Master access to a shared instance is disabled by default and can be enabled only as an explicit, scoped, revocable Master->shared link.
5. Creating or transferring a shared instance never copies Master memory, conversations, credentials, approvals, sessions, or private data.
6. Transfer payloads contain only explicitly selected bootstrap data.
7. Model output, prompts, previous approvals, or context cannot override instance isolation.
8. Isolation is enforced by a dedicated boundary outside the model.
