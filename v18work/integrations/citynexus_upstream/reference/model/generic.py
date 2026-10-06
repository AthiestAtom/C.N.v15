from enum import Enum
from pydantic import BaseModel, Field

ID_FORMAT = r"^[a-zA-Z0-9_-]+$"

class ApiResponse(BaseModel):
    response: str

class SimulationID(BaseModel):
    user_id: str = Field(min_length=3, max_length=40, pattern=ID_FORMAT)
    prediction_id: str = Field(min_length=3, max_length=40, pattern=ID_FORMAT)

class SimulationStatus(str, Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    FAILED = "Failed"
    NOT_AVAILABLE = "Not Available"

class StatusResponse(BaseModel):
    simulation_id: SimulationID
    status: SimulationStatus

class XAIResultFile(str, Enum):
    IMPACT = "impact"
    DIFFERENCE = "difference"
