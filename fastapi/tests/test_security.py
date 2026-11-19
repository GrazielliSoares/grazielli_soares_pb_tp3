
import os
import sys
from pathlib import Path

os.environ.setdefault(
    "JWT_SECRET_KEY",
    "chave-exclusiva-para-testes-locais"
)

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

import pytest
from pwdlib import PasswordHash
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool

from main import app
from database import get_session
from models.database_models import User, Prediction
from security.authentication import create_access_token
from limiter import limiter


@pytest.fixture
def client():
    # Banco SQLite temporário, isolado do banco real
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Cria um hash de senha válido para os testes
        password_hash = PasswordHash.recommended()
        senha_teste_hash = password_hash.hash("senha_teste_123")

        usuario1 = User(
            username="teste_usuario1",
            hashed_password=senha_teste_hash
        )

        usuario2 = User(
            username="teste_usuario2",
            hashed_password=senha_teste_hash
        )

        session.add(usuario1)
        session.add(usuario2)
        session.commit()

        session.refresh(usuario1)
        session.refresh(usuario2)

        prediction1 = Prediction(
            owner_id=usuario1.id,
            ticket_text="Cobrança incorreta",
            predicted_category="Billing"
        )

        prediction2 = Prediction(
            owner_id=usuario2.id,
            ticket_text="Solicitação de reembolso",
            predicted_category="Refund"
        )

        session.add(prediction1)
        session.add(prediction2)
        session.commit()

        session.refresh(prediction1)
        session.refresh(prediction2)

        dados = {
            "usuario1": usuario1.username,
            "prediction_usuario1": prediction1.id,
            "prediction_usuario2": prediction2.id,
        }

    def get_test_session():
        with Session(engine) as session:
            yield session

    # Limpa o contador antes de cada teste
    limiter._storage.reset()

    app.dependency_overrides[get_session] = get_test_session

    try:
        with TestClient(app) as test_client:
            yield test_client, dados
    finally:
        app.dependency_overrides.clear()

        # Evita que um teste interfira no próximo
        limiter._storage.reset()

        engine.dispose()


# Teste A — Acesso sem token JWT
def test_acesso_sem_token(client):
    test_client, dados = client

    response = test_client.get(
        f"/predictions/{dados['prediction_usuario1']}"
    )

    assert response.status_code == 401


# Teste B — Proteção contra BOLA
def test_acesso_prediction_outro_usuario(client):
    test_client, dados = client

    token = create_access_token(
        data={"sub": dados["usuario1"]}
    )

    response = test_client.get(
        f"/predictions/{dados['prediction_usuario2']}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404


# Teste C — Rejeição de campos extras
def test_campo_extra_rejeitado(client):
    test_client, dados = client

    token = create_access_token(
        data={"sub": dados["usuario1"]}
    )

    response = test_client.post(
        "/predict",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "text": "Preciso de ajuda com pagamento",
            "owner_id": 2
        }
    )

    assert response.status_code == 422

    assert any(
        erro["type"] == "extra_forbidden"
        for erro in response.json()["detail"]
    )


# Teste D — Credenciais inválidas
def test_login_credenciais_invalidas(client):
    test_client, dados = client

    response = test_client.post(
        "/auth/token",
        data={
            "username": dados["usuario1"],
            "password": "senha_incorreta"
        }
    )

    assert response.status_code == 401


# Teste E — Credenciais válidas
def test_login_credenciais_validas(client):
    test_client, dados = client

    response = test_client.post(
        "/auth/token",
        data={
            "username": dados["usuario1"],
            "password": "senha_teste_123"
        }
    )

    assert response.status_code == 200

    resposta = response.json()

    assert "access_token" in resposta
    assert resposta["token_type"] == "bearer"


# Teste F — Rate limiting de autenticação
def test_rate_limiting_autenticacao(client):
    test_client, dados = client

    respostas = []

    # Realiza mais de 10 tentativas em menos de 1 minuto
    for _ in range(12):
        response = test_client.post(
            "/auth/token",
            data={
                "username": dados["usuario1"],
                "password": "senha_incorreta"
            }
        )

        respostas.append(response.status_code)

    # Verifica se o limite foi aplicado
    assert 429 in respostas
