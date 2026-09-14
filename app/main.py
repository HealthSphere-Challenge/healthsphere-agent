import hmac
import logging
from contextlib import asynccontextmanager
from uuid import UUID

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.agent import AgentService, DependencyUnavailable
from app.config import Settings
from app.llm import OpenAICompatibleClient
from app.rag import MedicalRetriever, SparseVectorIndex
from app.schemas import AgentRequest, AgentResponse

logger = logging.getLogger("healthsphere.agent")


def create_app(settings: Settings | None = None, service: AgentService | None = None) -> FastAPI:
    configured = settings

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        nonlocal configured
        configured = configured or Settings()  # type: ignore[call-arg]
        if service is None:
            index = SparseVectorIndex.load(configured.index_path)
            app.state.service = AgentService(
                MedicalRetriever(index),
                OpenAICompatibleClient(
                    str(configured.llm_base_url),
                    configured.llm_api_key,
                    configured.llm_model,
                    configured.llm_timeout_seconds,
                ),
                str(index.metadata["corpus_version"]),
            )
        else:
            app.state.service = service
        app.state.settings = configured
        yield

    app = FastAPI(title="HealthSphere Agent", version="0.1.0", lifespan=lifespan)

    def error_response(status: int, code: str, message: str, request: Request) -> JSONResponse:
        raw = request.headers.get("X-Request-ID")
        request_id = raw if _valid_uuid4(raw) else "00000000-0000-4000-8000-000000000000"
        return JSONResponse(
            status_code=status,
            content={
                "error": {
                    "code": code,
                    "message": message,
                    "details": None,
                    "request_id": request_id,
                    "retry_after_seconds": None,
                }
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, _exc: RequestValidationError) -> JSONResponse:
        return error_response(
            422, "validation_error", "The request could not be validated.", request
        )

    @app.exception_handler(HTTPException)
    async def http_error(request: Request, exc: HTTPException) -> JSONResponse:
        code = "unauthorized" if exc.status_code == 401 else "validation_error"
        message = (
            "Service authentication failed."
            if exc.status_code == 401
            else "The request could not be validated."
        )
        return error_response(exc.status_code, code, message, request)

    def authorize(request: Request, authorization: str | None = Header(default=None)) -> None:
        expected = f"Bearer {request.app.state.settings.internal_token}"
        if authorization is None or not hmac.compare_digest(authorization, expected):
            raise HTTPException(status_code=401, detail="invalid service authentication")

    @app.exception_handler(DependencyUnavailable)
    async def unavailable(request: Request, _exc: DependencyUnavailable) -> JSONResponse:
        return error_response(
            503, "dependency_unavailable", "The assistant is temporarily unavailable.", request
        )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/ready")
    def ready(request: Request, _auth: None = Depends(authorize)) -> dict[str, object]:
        current = request.app.state.service
        return {
            "status": "ready",
            "index_version": current.retriever.index.metadata["index_version"],
            "corpus_version": current.corpus_version,
            "model_provider": current.llm.provider_name,
            "model_name": current.llm.model_name,
        }

    @app.post(
        "/internal/v1/agent/responses",
        response_model=AgentResponse,
        dependencies=[Depends(authorize)],
    )
    async def respond(
        payload: AgentRequest, request: Request, x_request_id: str = Header(alias="X-Request-ID")
    ) -> AgentResponse:
        if not _valid_uuid4(x_request_id) or str(payload.request_id) != x_request_id:
            raise HTTPException(
                status_code=422, detail="X-Request-ID must be UUIDv4 and equal request_id"
            )
        response = await request.app.state.service.respond(payload)
        logger.info(
            "agent_response request_id=%s response_type=%s retrieval_count=%d",
            payload.request_id,
            response.response_type,
            len(response.sources),
        )
        return response

    return app


def _valid_uuid4(value: str | None) -> bool:
    try:
        parsed = UUID(value or "")
        return parsed.version == 4 and str(parsed) == value
    except ValueError:
        return False


app = create_app()
