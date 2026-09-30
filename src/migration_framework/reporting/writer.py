from __future__ import annotations

from pathlib import Path

from migration_framework.contracts import MigrationReport


def write_report(report: MigrationReport, evidence_directory: Path) -> Path:
    evidence_directory.mkdir(parents=True, exist_ok=True)
    destination = evidence_directory / "migration-report.json"
    destination.write_text(report.model_dump_json(indent=2), encoding="utf-8")
    return destination
