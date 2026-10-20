
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from routes import auth, health, predict
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from limiter import limiter

app = FastAPI(
    title="API de Atendimento ao Cliente",
    description="API de classificação de chamados com autenticação JWT",
    version="2.0.0"
)

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

# CORS: somente origens explicitamente autorizadas
origens_permitidas = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origens_permitidas,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)


# Middleware para adicionar headers de segurança HTTP
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)

    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )

    response.headers["X-Frame-Options"] = "DENY"

    response.headers["X-Content-Type-Options"] = "nosniff"

    response.headers["Content-Security-Policy"] = (
        "default-src 'none'; "
        "frame-ancestors 'none'; "
        "base-uri 'none'; "
        "form-action 'self'"
    )

    return response


# Registro das rotas
app.include_router(auth.router)
app.include_router(health.router)
app.include_router(predict.router)
