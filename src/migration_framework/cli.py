from __future__ import annotations

import argparse
from pathlib import Path

from migration_framework.orchestration import analyze_project


def main() -> None:
    parser = argparse.ArgumentParser(description="Dataiku to Databricks migration framework")
    subparsers = parser.add_subparsers(dest="command", required=True)
    analyze = subparsers.add_parser("analyze", help="Analyze already-acquired local evidence")
    analyze.add_argument("--project-root", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "analyze":
        plan = analyze_project(args.project_root)
        print(plan.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
