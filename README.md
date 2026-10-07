# Mila Core

Technische Grundlage für das Mila-Projekt.

## Grundprinzip
Mila darf selbstständig recherchieren, analysieren und Aktionen vorbereiten.
Sensible Aktionen dürfen jedoch niemals ohne eine frische, ausdrückliche Zustimmung
des Nutzers ausgeführt werden.

Die Sicherheitsgrenze liegt außerhalb des KI-Modells: Das Modell kann eine Aktion
vorschlagen, aber der Security Gatekeeper entscheidet, ob sie ausgeführt werden darf.

## Sicherheitsstufen
- LOW: lesen, suchen, analysieren, Entwürfe erstellen
- MEDIUM: vorbereiten oder reversible interne Änderungen
- HIGH: sensible externe oder irreversible Aktionen

HIGH erfordert immer eine neue ausdrückliche Zustimmung.
Keine Zustimmung oder unklare Zustimmung bedeutet: NICHT AUSFÜHREN.

## V10 – External Gateway
V10 adds a provider-neutral outbound boundary for future real services. Providers and hosts are allowlisted, HTTPS is mandatory, and credentials are supplied separately. No live API call is required for the test suite, so V10 can be developed before API credits are available.
