
# Echter Search Provider – nächste Integrationsstufe

Der bisherige Mock-Provider bleibt für lokale Tests erhalten.

Dieser neue Adapter ermöglicht die spätere Anbindung eines echten
Suchdienstes über eine konfigurierte HTTP-API.

## Noch bewusst offen

Wir legen hier noch keinen konkreten Anbieter fest. Dafür müssen wir
zunächst entscheiden, welchen Suchdienst Mila verwenden soll und welche
Zugangsdaten bzw. Kosten damit verbunden sind.

Der API-Schlüssel darf niemals im Quellcode stehen. Er gehört später in
sichere Umgebungsvariablen bzw. einen Secret Store.

## Sicherheitsgrenze

Der Search Provider darf ausschließlich Suchanfragen ausführen und
Suchergebnisse zurückgeben. Er bekommt keine Berechtigung für sensible
Aktionen.

Eine Suche ist niemals eine Zustimmung zu einer externen Aktion.
