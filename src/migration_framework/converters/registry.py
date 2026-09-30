from __future__ import annotations

from collections.abc import Callable

from migration_framework.contracts import RecipeContract
from migration_framework.ir import Operation, TransformationPlan

Converter = Callable[[RecipeContract], TransformationPlan]


def generic_converter(recipe: RecipeContract) -> TransformationPlan:
    operations = (
        [Operation(kind=p.processor_type, parameters=p.parameters) for p in recipe.processors]
        if recipe.recipe_type == "shaker"
        else [Operation(kind=recipe.recipe_type, parameters=recipe.configuration)]
    )
    return TransformationPlan(recipe_id=recipe.recipe_id, inputs=recipe.inputs, outputs=recipe.outputs, operations=operations)


class ConverterRegistry:
    def __init__(self) -> None:
        self._converters: dict[str, Converter] = {}

    def register(self, recipe_type: str, converter: Converter) -> None:
        self._converters[recipe_type] = converter

    def convert(self, recipe: RecipeContract) -> TransformationPlan:
        if recipe.recipe_type not in self._converters:
            raise KeyError(f"No converter registered for {recipe.recipe_type}")
        return self._converters[recipe.recipe_type](recipe)


def default_registry() -> ConverterRegistry:
    registry = ConverterRegistry()
    for recipe_type in ("shaker", "distinct", "split", "vstack", "grouping", "pivot", "join", "window"):
        registry.register(recipe_type, generic_converter)
    return registry
