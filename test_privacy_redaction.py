from privacy_redaction import PrivacyRedactor
def test_redact_key(): assert "secret" not in PrivacyRedactor().redact("api_key=secret")
def test_keep_normal_text(): assert PrivacyRedactor().redact("Hallo Welt")=="Hallo Welt"
