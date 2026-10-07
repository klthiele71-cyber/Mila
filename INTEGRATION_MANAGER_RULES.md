# Mila Integration Manager

Diese Schicht verbindet den Development Agent mit einer späteren
Ausführungs-/Deploymentschicht.

## Grundprinzip
Der Integration Manager bewertet Änderungen und bereitet deren Integration
vor. Er schreibt selbst keinen Projektcode und führt keine Dateiänderungen aus.

## Sicherheitsregeln
- Fehlgeschlagene Tests blockieren die Integration.
- Geschützte Security-Komponenten sind blockiert.
- Sicherheitsrelevante Änderungen werden nicht automatisch integriert.
- Eine vorherige Zustimmung wird nicht gespeichert oder wiederverwendet.
- `approval_consumed` bleibt bewusst `False`.
- Die tatsächliche Ausführung gehört in eine getrennte äußere Schicht.
