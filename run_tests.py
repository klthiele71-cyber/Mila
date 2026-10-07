import importlib
import inspect
import sys

TEST_MODULES = [
    "test_security",
    "test_task_context",
    "test_memory",
    "test_research",
    "test_dialog_decision",
    "test_integration",
    "test_search_provider",
    "test_search_integration",
    "test_real_search_provider",
    "test_model_adapter",
    "test_ai_model_integration",
    "test_development_agent",
    "test_integration_manager",
    "test_mila_orchestrator",
    "test_execution_engine",
    "test_audit_log",
    "test_rollback",
    "test_v9_integration",
    "test_external_gateway",
    "test_provider_registry",
    "test_request_policy",
    "test_mobile_gateway",
    "test_operations",
    "test_session_manager",
    "test_credential_store",
    "test_approval_protocol",
    "test_diagnostics",
    "test_config_validator",
    "test_release_gate",
    "test_provider_health",
    "test_model_router",
    "test_conversation_pipeline",
    "test_memory_context_bridge",
    "test_speech_interface",
    "test_mobile_session_integration",
    "test_privacy_redaction",
    "test_resilience_queue",
    "test_system_integration",
    "test_release_candidate",
    "test_openai_responses_provider",
    "test_live_api_preflight",
    "test_openai_http_transport",
    "test_instance_isolation",
]

passed = 0
failed = 0

for module_name in TEST_MODULES:
    module = importlib.import_module(module_name)
    for name, fn in inspect.getmembers(module, inspect.isfunction):
        if name.startswith("test_"):
            try:
                fn()
                print(f"PASS  {module_name}.{name}")
                passed += 1
            except Exception as exc:
                print(f"FAIL  {module_name}.{name}: {exc}")
                failed += 1

print()
print(f"Ergebnis: {passed} bestanden, {failed} fehlgeschlagen")
sys.exit(1 if failed else 0)
