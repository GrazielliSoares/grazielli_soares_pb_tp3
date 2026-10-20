from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    access_token: str
    token_type: str


class PredictRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str


class PredictResponse(BaseModel):
    intent: str
    confidence: float