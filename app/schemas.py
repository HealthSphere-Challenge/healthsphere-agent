from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class RecentTurn(StrictModel):
    role: Literal["user", "assistant"]
    content: Annotated[str, Field(min_length=1, max_length=2000)]


class AssessmentContext(StrictModel):
    target_id: Literal["incident_essential_hypertension_5y_v1"]
    score: Annotated[float, Field(ge=0, le=1, allow_inf_nan=False)]
    score_type: Literal["uncalibrated_experimental_probability_estimate"]
    calibrated: Literal[False]
    model_version: Literal["hypertension_5y_v1.0.0"]
    prediction_horizon_days: Literal[1825]


class HealthContext(StrictModel):
    profile: dict[str, object] | None = None
    measurements: Annotated[list[dict[str, object]], Field(max_length=20)] = Field(
        default_factory=list
    )
    assessment: AssessmentContext | None = None


class AgentRequest(StrictModel):
    schema_version: Literal["1.0"]
    request_id: UUID
    conversation_ref: UUID
    user_message: Annotated[str, Field(min_length=1, max_length=2000)]
    recent_turns: Annotated[list[RecentTurn], Field(max_length=6)] = Field(default_factory=list)
    health_context: HealthContext


class Source(StrictModel):
    source_id: str
    title: str
    url: HttpUrl | None


class Safety(StrictModel):
    urgent: bool
    reason: str | None


class Provenance(StrictModel):
    corpus_version: str
    retrieval_version: str
    prompt_version: str
    model_provider: str
    model_name: str
    generated_at: datetime


class AgentResponse(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    request_id: UUID
    response_type: Literal["answer", "follow_up", "abstention", "urgent"]
    content: str
    sources: list[Source]
    safety: Safety
    uncertainty: str
    provenance: Provenance

    @model_validator(mode="after")
    def consistent_state(self) -> "AgentResponse":
        if self.response_type == "urgent" and not self.safety.urgent:
            raise ValueError("urgent responses require urgent safety state")
        if self.response_type != "urgent" and self.safety.urgent:
            raise ValueError("non-urgent responses cannot set urgent safety state")
        if self.response_type == "answer" and not self.sources:
            raise ValueError("grounded answers require sources")
        return self


class ErrorBody(StrictModel):
    code: str
    message: str
    details: None = None
    request_id: UUID
    retry_after_seconds: int | None = None


class ErrorEnvelope(StrictModel):
    error: ErrorBody
