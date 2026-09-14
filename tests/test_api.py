from pathlib import Path

from fastapi.testclient import TestClient

from app.agent import AgentService
from app.config import Settings
from app.main import create_app
from app.rag import MedicalRetriever
from tests.conftest import FakeLLM

REQUEST_ID = "c4a760a8-7d0b-4f98-9652-244be1ebcc2e"
TOKEN = "a-secure-internal-token-for-tests"


def payload(message: str = "What is hypertension blood pressure?") -> dict:
    return {
        "schema_version": "1.0",
        "request_id": REQUEST_ID,
        "conversation_ref": "7a19544c-e55f-4ea8-96b9-557575027fb4",
        "user_message": message,
        "recent_turns": [],
        "health_context": {"profile": None, "measurements": [], "assessment": None},
    }


def client_for(service: AgentService) -> TestClient:
    settings = Settings(internal_token=TOKEN, llm_api_key="test-key", index_path=Path("unused"))
    return TestClient(create_app(settings, service))


def headers(request_id: str = REQUEST_ID) -> dict[str, str]:
    return {"Authorization": f"Bearer {TOKEN}", "X-Request-ID": request_id}


def test_health_readiness_and_auth(service):
    with client_for(service) as client:
        assert client.get("/health").json() == {"status": "ok"}
        assert client.get("/ready").status_code == 401
        ready = client.get("/ready", headers=headers())
        assert (
            ready.status_code == 200 and ready.json()["index_version"] == "medquad-sparse-cosine-v1"
        )


def test_contract_answer_and_request_correlation(service):
    with client_for(service) as client:
        response = client.post("/internal/v1/agent/responses", headers=headers(), json=payload())
        assert response.status_code == 200
        assert (
            response.json()["request_id"] == REQUEST_ID
            and response.json()["response_type"] == "answer"
        )
        mismatch = client.post(
            "/internal/v1/agent/responses",
            headers=headers("11111111-1111-4111-8111-111111111111"),
            json=payload(),
        )
        assert (
            mismatch.status_code == 422 and mismatch.json()["error"]["code"] == "validation_error"
        )


def test_strict_schema_invalid_score_and_auth_are_canonical(service):
    body = payload()
    body["unexpected"] = "rejected"
    with client_for(service) as client:
        invalid = client.post("/internal/v1/agent/responses", headers=headers(), json=body)
        assert invalid.status_code == 422 and invalid.json()["error"]["request_id"] == REQUEST_ID
        assessment_body = payload("Explain my assessment")
        assessment_body["health_context"]["assessment"] = {
            "target_id": "incident_essential_hypertension_5y_v1",
            "score": 1.1,
            "score_type": "uncalibrated_experimental_probability_estimate",
            "calibrated": False,
            "model_version": "hypertension_5y_v1.0.0",
            "prediction_horizon_days": 1825,
        }
        assert (
            client.post(
                "/internal/v1/agent/responses", headers=headers(), json=assessment_body
            ).status_code
            == 422
        )
        unauthorized = client.post(
            "/internal/v1/agent/responses", headers={"X-Request-ID": REQUEST_ID}, json=payload()
        )
        assert (
            unauthorized.status_code == 401
            and unauthorized.json()["error"]["code"] == "unauthorized"
        )


def test_all_response_states(service):
    with client_for(service) as client:
        for message, expected in [
            ("It hurts", "follow_up"),
            ("unrelated spaceship taxation", "abstention"),
            ("I cannot breathe", "urgent"),
        ]:
            response = client.post(
                "/internal/v1/agent/responses", headers=headers(), json=payload(message)
            )
            assert response.status_code == 200 and response.json()["response_type"] == expected


def test_provider_failure_uses_safe_canonical_error(index):
    service = AgentService(
        MedicalRetriever(index, minimum_score=0.01), FakeLLM(fail=True), "fixture-v1"
    )
    with client_for(service) as client:
        response = client.post("/internal/v1/agent/responses", headers=headers(), json=payload())
        assert response.status_code == 503
        assert response.json()["error"]["message"] == "The assistant is temporarily unavailable."
        assert "secret provider failure" not in response.text
