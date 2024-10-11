from pydantic import BaseModel, Field


class TunerSchema(BaseModel):
    type: str = Field("TPE", description="Optimization type")
    epochs: int = Field(10, description="Optimization epochs")
    direction: str = Field("maximize", description="Optimization direction")


class OptimizationStateSchema(BaseModel):
    trial: int = Field(description="Optimization current trial")


class OptimizationInSchema(BaseModel):
    name: str = Field(description="Optimization name")
    tuner: TunerSchema = Field(description="Tuner metadata")
    metadata: dict = Field(description="Optimization metadata")
