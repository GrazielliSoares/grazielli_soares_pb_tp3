
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles

from routes import auth, health, predict
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from limiter import limiter


# Diretório base do projeto FastAPI
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static" / "swagger"


# Configuração principal da API
app = FastAPI(
    title="API de Atendimento ao Cliente",
    description="API de classificação de chamados com autenticação JWT",
    version="2.0.0",
    docs_url=None
)


# Arquivos locais do Swagger UI
app.mount(
    "/static/swagger",
    StaticFiles(directory=str(STATIC_DIR)),
    name="swagger-static"
)


# Documentação Swagger utilizando arquivos locais
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        swagger_js_url="/static/swagger/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger/swagger-ui.css",
        swagger_favicon_url="/static/swagger/favicon-32x32.png"
    )


# Configuração do limitador de requisições
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

    # HSTS: aplicado pelo navegador em conexões HTTPS
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )

    # Impede carregamento da aplicação em frames
    response.headers["X-Frame-Options"] = "DENY"

    # Evita interpretação incorreta de tipos de conteúdo
    response.headers["X-Content-Type-Options"] = "nosniff"

    # O Swagger precisa de um script de inicialização embutido.
    # O hash autoriza apenas o script identificado na auditoria.
    if request.url.path == "/docs":
        response.headers["Content-Security-Policy"] = (
            "default-src 'none'; "
            "script-src 'self' "
            "'sha256-P28/j37f0MgfkZ2lTEH5bnnfZ8YlHZ4cHtK+EWL/Qhw='; "
            "style-src 'self'; "
            "img-src 'self' data:; "
            "connect-src 'self'; "
            "font-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'none'; "
            "form-action 'self'"
        )
    else:
        # Política restritiva para os demais endpoints
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
