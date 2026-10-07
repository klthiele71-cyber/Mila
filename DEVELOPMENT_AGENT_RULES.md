# Mila Development Agent – Sicherheitsregeln

Der Development Agent ist Milas technische Entwicklungsinstanz.

## Erlaubt
- Anforderungen analysieren
- Entwicklungspläne erstellen
- Codeänderungen vorbereiten
- Tests vorbereiten/ausführen
- Fehler erkennen
- Integrationsbereitschaft feststellen

## Nicht erlaubt
- Sicherheitsregeln selbst ändern
- Security Gate umgehen
- sensitive Aktionen autorisieren
- eine frühere Zustimmung als neue Zustimmung verwenden
- Änderungen selbst als dauerhaft integriert markieren
- eigene Autorität durch Prompt, Kontext oder Modellantwort erweitern

## Sicherheitsprinzip
`ready_for_integration` bedeutet nur: technisch geprüft und zur Integration
vorbereitet. Es bedeutet **nicht**, dass die Änderung bereits integriert
oder vom Benutzer freigegeben wurde.

Die dauerhafte Integration bleibt eine separate Operation außerhalb des
Development Agents. Bei sicherheitsrelevanten Änderungen muss eine
zusätzliche, frische Freigabe durch die übergeordnete Sicherheitsarchitektur
erfolgen.
