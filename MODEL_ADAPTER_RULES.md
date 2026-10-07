# Mila AI Model Adapter – Regeln

## Zweck
Der Model Adapter verbindet Mila-Core-Daten mit einem später austauschbaren
KI-Modellanbieter. In dieser Entwicklungsstufe wird ausschließlich ein
Offline-Mock verwendet.

## Sicherheitsprinzip
Das Modell ist **nicht vertrauenswürdig für Autorisierung**.

- Das Modell darf Antworten und Aktionsvorschläge liefern.
- Das Modell darf niemals selbst eine sensitive Aktion freigeben.
- Eine frühere Zustimmung des Nutzers wird nicht als aktuelle Zustimmung
  interpretiert.
- Sensitive Aktionen müssen weiterhin durch das externe Security Gate.
- Der Adapter besitzt absichtlich keine `authorize()`- oder
  `execute()`-Methode.
- Ein späterer echter Provider ersetzt nur die Modellkommunikation; er
  ersetzt nicht das Security Gate.

## Datenfluss
Benutzer -> Mila Core -> AIModelService -> ModelProvider
-> ModelResponse -> Mila Core -> Security Gate (falls Aktion vorgeschlagen)

Der Adapter ist provider-neutral. Dadurch kann später z.B. ein OpenAI-
Provider angeschlossen werden, ohne die Sicherheitsarchitektur zu ändern.
