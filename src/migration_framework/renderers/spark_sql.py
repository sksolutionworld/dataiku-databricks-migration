"""Conservative Spark SQL renderer for supported IR operations."""

from __future__ import annotations

from migration_framework.ir import TransformationPlan


def render(plan: TransformationPlan) -> str:
    header = f"-- Generated from Dataiku recipe: {plan.recipe_id}\n"
    if not plan.operations:
        return header + "-- No operations\n"
    operation = plan.operations[0]
    if operation.kind == "distinct":
        return header + f"SELECT DISTINCT * FROM {plan.inputs[0]};\n"
    if operation.kind == "vstack":
        return header + "\nUNION ALL\n".join(f"SELECT * FROM {name}" for name in plan.inputs) + ";\n"
    return header + f"-- {operation.kind} requires its specialized renderer; do not execute this placeholder.\n"
