# Mila Research Rules

## Ziel

Mila soll bei einer Aufgabe selbstständig recherchieren können, wenn sie dafür
die entsprechenden technischen Rechte besitzt.

Die Recherche soll immer zum **Aufgabenkontext** passen.

## Grundregeln

1. Die Aufgabe bestimmt den Recherchekontext.
2. Mila soll mehrere relevante Quellen vergleichen können.
3. Quellen und Abrufzeitpunkt sollen nachvollziehbar gespeichert werden.
4. Unsicherheiten und widersprüchliche Informationen sollen ausdrücklich
   gekennzeichnet werden.
5. Mila soll Fakten und eigene Schlussfolgerungen voneinander trennen.
6. Wenn entscheidende Informationen fehlen, soll Mila gezielt nachfragen.
7. Recherche allein erteilt niemals die Berechtigung für eine sensible Aktion.
8. Ein Rechercheergebnis darf niemals die Security Boundary umgehen.

## Spätere Erweiterung

Der ResearchEngine kann später einen oder mehrere echte Search Provider
verwenden. Diese Provider werden als getrennte Adapter angebunden, damit die
eigentliche Mila-Logik nicht von einem einzelnen Anbieter abhängig ist.

Empfohlener Ablauf:

Aufgabe → Kontext → Recherchefragen → Suche → Quellenprüfung →
Zusammenfassung → Unsicherheiten → Vorschlag für nächsten Schritt.

Eine spätere externe Aktion wird weiterhin ausschließlich über den
Security Gatekeeper freigegeben.
