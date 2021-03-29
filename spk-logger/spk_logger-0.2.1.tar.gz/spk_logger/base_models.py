from pydantic import BaseModel 

class LogInfo(BaseModel):
    log_type: str
    user: str
    project: str
    date: str
    info: dict

class Prediction(BaseModel):
    prediction: dict
    model_id: str
    process_time: float
    prediction_date: str
    user: str
    model_features: dict

class LogInput(BaseModel):
    log_type: str
    user: str
    input_raw: dict

class LogPrediction(BaseModel):
    log_type: str
    predict: Prediction
    input: LogInput
    user: str
    
class LogPredictionError(BaseModel):
    log_type: str 
    msg_error: str
    model_id: str
    date: str
    user:str
    input: LogInput

