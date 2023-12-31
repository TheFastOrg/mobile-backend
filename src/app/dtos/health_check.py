from pydantic import BaseModel, Field


class HealthCheckModel(BaseModel):
    title: str = Field(..., description="API title")
    description: str = Field(..., description="Brief description of the API")
    version: str = Field(..., description="API version number")
    status: str = Field(..., description="API current status")
