import re
class PrivacyRedactor:
    def redact(self,text):
        text=re.sub(r"(?i)(api[_-]?key|token|password)\s*[:=]\s*[^\s,;]+",r"\1=[REDACTED]",text)
        return text
