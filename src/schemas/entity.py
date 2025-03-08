from pydantic import BaseModel, ConfigDict


class EntityBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
