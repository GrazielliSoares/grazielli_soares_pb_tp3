
import os
import sys
from pathlib import Path

os.environ.setdefault("JWT_SECRET_KEY", "chave-exclusiva-para-testes-locais")

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool

from main import app
from database import get_session
from models.database_models import User, Prediction
from security.authentication import create_access_token


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
        usuario1 = User(
            username="teste_usuario1",
            hashed_password="hash_teste"
        )

        usuario2 = User(
            username="teste_usuario2",
            hashed_password="hash_teste"
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

    app.dependency_overrides[get_session] = get_test_session

    try:
        with TestClient(app) as test_client:
            yield test_client, dados
    finally:
        app.dependency_overrides.clear()
        engine.dispose()


# Teste A — Acesso sem token JWT
def test_acesso_sem_token(client):
    test_client, dados = client

    response = test_client.get(
        f"/predictions/{dados['prediction_usuario1']}"
    )

    assert response.status_code == 401


# Teste B — Acesso a recurso de outro usuário
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


# Teste C — Campo extra no body da requisição
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
