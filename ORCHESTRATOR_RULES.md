# Mila Orchestrator – Regeln

Der Orchestrator ist die zentrale Koordinationsschicht von Mila.

## Aufgabe
Er verbindet:
- Dialog/Entscheidung
- Modelladapter
- Development Agent
- Integration Manager

## Keine neue Autorität
Der Orchestrator darf keine bestehende Sicherheitsgrenze ersetzen.

- Er führt keine sensitiven Aktionen aus.
- Er kann nur Entwicklungs- und Integrationszustände weiterreichen.
- `INTEGRATION_READY` bedeutet nicht "integriert".
- Security bleibt außerhalb des Modells und außerhalb des Orchestrators
  maßgeblich.
- Sicherheitsrelevante Änderungen bleiben blockiert und benötigen die
  dafür vorgesehene übergeordnete Sicherheitsprüfung.
