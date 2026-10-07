from speech_interface import SpeechInterface
def test_transcribe(): assert SpeechInterface().transcribe("Hallo").text=="Hallo"
def test_confidence_validation():
 try: SpeechInterface().transcribe("x",1.5); assert False
 except ValueError: pass
def test_synthesize(): assert SpeechInterface().synthesize("x")["format"]=="audio-placeholder"
