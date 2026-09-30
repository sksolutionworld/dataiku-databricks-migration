"""Canonical contracts independent of raw Dataiku JSON shapes."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class MigrationStatus(StrEnum):
    DISCOVERED = "DISCOVERED"
    ANALYZED = "ANALYZED"
    PLANNED = "PLANNED"
    CONVERTED = "CONVERTED"
    VALIDATED = "VALIDATED"
    REQUIRES_REVIEW = "REQUIRES_REVIEW"
    FAILED = "FAILED"


class DatasetContract(BaseModel):
    name: str
    role: str = "intermediate"
    metadata: dict[str, Any] = Field(default_factory=dict)


class ProcessorContract(BaseModel):
    processor_type: str
    parameters: dict[str, Any] = Field(default_factory=dict)
    disabled: bool = False


class RecipeContract(BaseModel):
    recipe_id: str
    recipe_name: str
    recipe_type: str
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    configuration: dict[str, Any] = Field(default_factory=dict)
    processors: list[ProcessorContract] = Field(default_factory=list)
    source_code: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ProjectContract(BaseModel):
    project_key: str
    datasets: list[DatasetContract] = Field(default_factory=list)
    recipes: list[RecipeContract] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class DependencyContract(BaseModel):
    upstream_dataset: str
    recipe_id: str
    downstream_dataset: str


class CapabilityResult(BaseModel):
    recipe_id: str
    recipe_type: str
    disposition: str
    reason: str


class MigrationPlan(BaseModel):
    project_key: str
    status: MigrationStatus = MigrationStatus.PLANNED
    ordered_recipe_ids: list[str]
    capabilities: list[CapabilityResult]


class ValidationResult(BaseModel):
    check: str
    status: str
    expected: Any = None
    actual: Any = None
    details: dict[str, Any] = Field(default_factory=dict)


class MigrationReport(BaseModel):
    project_key: str
    status: MigrationStatus
    converted_recipes: list[str] = Field(default_factory=list)
    review_items: list[str] = Field(default_factory=list)
    validations: list[ValidationResult] = Field(default_factory=list)
