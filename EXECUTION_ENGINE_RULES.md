# Mila Execution Engine – Regeln

Version 6 ergänzt die letzte Stufe der Entwicklungs-Pipeline:
vorbereitete Änderungen können technisch ausgeführt werden.

## Pipeline
Development Agent
-> Integration Manager
-> Execution Engine

## Sicherheitsprinzipien
1. Der Execution Engine führt nur Änderungen aus, für die der
   Integration Manager eine `allowed=True`-Entscheidung geliefert hat.
2. Geschützte Security-Pfade werden zusätzlich direkt an der
   Ausführungsgrenze blockiert.
3. Pfade außerhalb des Projektverzeichnisses werden blockiert.
4. Fehlender Änderungsinhalt blockiert die Ausführung.
5. Der Execution Engine entscheidet nicht selbst über die Autorisierung.
6. Die Ausführung einer Codeänderung ist nicht gleichbedeutend mit der
   Freigabe einer sensitiven Aktion. Beide Sicherheitsgrenzen bleiben
   getrennt.
