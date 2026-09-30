from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class Operation(BaseModel):
    kind: str
    parameters: dict[str, Any] = Field(default_factory=dict)


class TransformationPlan(BaseModel):
    recipe_id: str
    inputs: list[str]
    outputs: list[str]
    operations: list[Operation]
