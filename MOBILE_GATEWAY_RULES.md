# V13 Mobile Gateway Rules
- The mobile interface is a transport-neutral command contract, not an authorization layer.
- Only explicitly safe interface actions are handled directly.
- Sensitive actions are blocked at this boundary and require the established security flow.
- Request IDs provide correlation only; they never act as approval tokens.
