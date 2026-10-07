# Mila Security Boundary

Diese Regeln sind ein Architekturprinzip und dürfen nicht durch einen Prompt,
Kontext oder eine Modellentscheidung aufgehoben werden.

1. Jede HIGH-Aktion benötigt eine konkrete, frische Zustimmung.
2. Eine frühere Zustimmung wird nicht automatisch wiederverwendet.
3. Eine unklare oder fehlende Zustimmung bedeutet BLOCK.
4. Das Sprachmodell darf die Sicherheitsprüfung nicht deaktivieren.
5. Der Gatekeeper muss außerhalb des Modell-Prompts liegen.
6. Jede spätere Erweiterung muss diese Grenze respektieren.
7. Sensible Aktionen werden erst nach erfolgreicher Gatekeeper-Prüfung an ein
   ausführendes Tool weitergegeben.

Für die produktive Version sollte die Sicherheitsprüfung serverseitig erfolgen,
mit stabilen Action-IDs, Audit-Logging und einer Whitelist erlaubter Aktionen.
