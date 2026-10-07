# Rollback / Recovery Rules

1. Rollback is limited to changes that were explicitly snapshotted by the execution layer.
2. Rollback never grants authorization and never reuses an approval.
3. Protected security paths remain technically blocked during snapshot and rollback.
4. Paths must remain inside the configured project root.
5. A rollback can be performed at most once for a given snapshot; repeating it is a no-op.
6. Unknown rollback identifiers are blocked.
7. Recovery records describe what happened; they do not change the security gate.
