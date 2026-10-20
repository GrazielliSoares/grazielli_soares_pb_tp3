
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from database import get_session
from models.database_models import User, Prediction
from models.schemas import PredictRequest, PredictResponse
from security.authentication import verify_token

router = APIRouter()


# Criar uma prediction
@router.post("/predict", response_model=PredictResponse)
def predict_intent(
    request: PredictRequest,
    user: User = Depends(verify_token),
    session: Session = Depends(get_session)
):
    intent = "Billing_Issue"
    confidence = 0.95

    prediction = Prediction(
        owner_id=user.id,
        ticket_text=request.text,
        predicted_category=intent
    )

    session.add(prediction)
    session.commit()
    session.refresh(prediction)

    return PredictResponse(
        intent=intent,
        confidence=confidence
    )


# Consultar uma prediction pelo ID
# Proteção contra BOLA (Broken Object Level Authorization)
@router.get("/predictions/{prediction_id}")
def get_prediction(
    prediction_id: int,
    user: User = Depends(verify_token),
    session: Session = Depends(get_session)
):
    prediction = session.get(Prediction, prediction_id)

    # Verifica se a prediction existe
    if prediction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction não encontrada"
        )

    # Verifica se pertence ao usuário autenticado
    if prediction.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prediction não encontrada"
        )

    return prediction
