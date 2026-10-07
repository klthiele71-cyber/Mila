from dataclasses import dataclass
@dataclass(frozen=True)
class SpeechInput:
    text: str; confidence: float
class SpeechInterface:
    def transcribe(self,text,confidence=1.0):
        if confidence < 0 or confidence > 1: raise ValueError("confidence")
        return SpeechInput(text,confidence)
    def synthesize(self,text):
        return {"text":text,"format":"audio-placeholder"}
