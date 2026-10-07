# Mila Search Provider

## Ziel

Der Search Provider ist die technische Schnittstelle zwischen Mila und einer
externen Suchquelle.

Der Provider ist bewusst austauschbar.

## Architektur

Mila Research Engine
        ↓
Search Service
        ↓
Search Provider
        ↓
externe Suchquelle

Dadurch bleibt die Mila-Logik unabhängig vom konkreten Suchanbieter.

## Sicherheitsregeln

- Eine Suche ist nicht automatisch eine Erlaubnis für eine externe Aktion.
- Suchergebnisse dürfen niemals die Security Boundary umgehen.
- URLs und Quellen sollen nachvollziehbar erhalten bleiben.
- Der Abrufzeitpunkt soll gespeichert werden.
- Fehler und fehlende Ergebnisse müssen an Mila zurückgegeben werden.
- Ein Suchtreffer ist nicht automatisch eine verifizierte Tatsache.

## Nächster technischer Schritt

Der `MockSearchProvider` wird später durch einen echten Provider ersetzt.
Dieser kann beispielsweise eine Such-API oder einen anderen zulässigen
Suchdienst verwenden.

Dafür werden wir dann die Authentifizierung und gegebenenfalls Kosten
separat konfigurieren.

## Wichtig

Der Provider darf nur suchen und Ergebnisse zurückgeben.
Er darf keine E-Mails senden, Käufe ausführen, Dateien löschen oder andere
sensible Aktionen durchführen.
