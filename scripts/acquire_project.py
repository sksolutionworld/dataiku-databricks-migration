import os
import shutil
import zipfile
from pathlib import Path

try:
    from dataikuapi import DSSClient
except ImportError as exc:
    raise SystemExit(
        "Missing dependency 'dataikuapi'. Install it with: "
        "python -m pip install -r requirements.txt"
    ) from exc


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

PROJECT_KEY = "TITANIC_MIGRATION_POC"

# Keep these outside the source code.
# Example:
#   DATAIKU_URL
#   DATAIKU_API_KEY
DATAIKU_URL = os.environ["DATAIKU_URL"]
DATAIKU_API_KEY = os.environ["DATAIKU_API_KEY"]

BASE_DIR = Path(__file__).resolve().parent

# Final location expected by our migration framework
PROJECT_DIR = BASE_DIR / "projects" / PROJECT_KEY
RAW_DIR = PROJECT_DIR / "dataiku" / "raw"
EXPORT_DIR = RAW_DIR / "project_export"

# Temporary ZIP
ZIP_FILE = RAW_DIR / f"{PROJECT_KEY}_export.zip"


# ---------------------------------------------------------
# Create directories
# ---------------------------------------------------------

RAW_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# Connect to Dataiku
# ---------------------------------------------------------

client = DSSClient(
    DATAIKU_URL,
    api_key=DATAIKU_API_KEY,
)

# ---------------------------------------------------------
# Download Dataiku project ZIP
# ---------------------------------------------------------

print(f"Downloading Dataiku project: {PROJECT_KEY}")

project = client.get_project(PROJECT_KEY)

project.export_to_file(str(ZIP_FILE))

print(f"Project archive downloaded: {ZIP_FILE}")


# ---------------------------------------------------------
# Clean previous extracted export
# ---------------------------------------------------------

if EXPORT_DIR.exists():
    print(f"Removing previous export: {EXPORT_DIR}")
    shutil.rmtree(EXPORT_DIR)

EXPORT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# Extract ZIP
# ---------------------------------------------------------

print("Extracting project archive...")

with zipfile.ZipFile(ZIP_FILE, "r") as zip_ref:
    zip_ref.extractall(EXPORT_DIR)

print(f"Project extracted to: {EXPORT_DIR}")


# ---------------------------------------------------------
# Remove ZIP after successful extraction
# ---------------------------------------------------------

ZIP_FILE.unlink()

print("Temporary ZIP removed.")


# ---------------------------------------------------------
# Complete
# ---------------------------------------------------------

print()
print("Dataiku project acquisition completed successfully.")
print(f"Project Key : {PROJECT_KEY}")
print(f"Raw Export  : {EXPORT_DIR}")
