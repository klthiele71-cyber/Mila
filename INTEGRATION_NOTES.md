# Integration in den Mila-Core

Der TaskContextEngine ist bewusst von der Ausführung getrennt.

Empfohlener Ablauf:

1. Nutzer erstellt eine Aufgabe.
2. Mila erfasst Ziel und vorhandenen Kontext.
3. Mila erkennt fehlende Informationen.
4. Mila fragt gezielt nach, wenn diese Informationen für die Aufgabe erforderlich sind.
5. Mila erstellt Recherche- oder Arbeitsschritte.
6. Recherche und Analyse können selbstständig erfolgen, sofern die jeweiligen Rechte vorhanden sind.
7. Sobald eine konkrete Aktion ausgeführt werden soll, wird diese Aktion an den Security Gatekeeper übergeben.
8. Der Gatekeeper entscheidet unabhängig vom Modell:
   - LOW/MEDIUM: nach den jeweils definierten Regeln
   - HIGH: immer frische, ausdrückliche Zustimmung
9. Ohne gültige Zustimmung wird die Aktion blockiert.

Wichtig:
Der TaskContextEngine darf niemals selbst ein sensibles externes Tool aufrufen.
Er verwaltet Kontext und plant; die Ausführung bleibt getrennt.
