from pydantic import BaseModel
from typing import List

# Define the request model for route calculation
class RouteResponse(BaseModel):
    status: str
    start_point: str
    end_point: str
    path: List[str]
    estimated_time_seconds: int