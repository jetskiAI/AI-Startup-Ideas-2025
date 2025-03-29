import os
import requests
from pathlib import Path
from datetime import datetime

API_URL = "https://jetskiapi.fly.dev/process"
BASE_DIR = Path(__file__).resolve().parent.parent
SUBMISSIONS_DIR = BASE_DIR / "submissions"
TEMPLATE_PATH = BASE_DIR / "assets" / "case_study_template.md"
OUTPUT_DIR = BASE_DIR / "case-studies"
ARCHIVE_DIR = BASE_DIR / "archive"

def process():
    # Get the first .md file from submissions/
    submission_files = list(SUBMISSIONS_DIR.glob("*.md"))
    if not submission_files:
        print("✅ No new submissions.")
        return

    submission_path = submission_files[0]
    print(f"📨 Processing {submission_path.name}")

    with open(submission_path, "rb") as sub_file, open(TEMPLATE_PATH, "rb") as tpl_file:
        files = {
            "submission": sub_file,
            "template": tpl_file
        }
        response = requests.post(API_URL, files=files)

    if response.status_code == 200:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{submission_path.stem}_filled_{timestamp}.md"
        output_path = OUTPUT_DIR / output_filename

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"✅ Saved case study to: {output_path.name}")

        archive_path = ARCHIVE_DIR / submission_path.name
        submission_path.rename(archive_path)
        print(f"📦 Moved submission to archive: {archive_path.name}")
    else:
        print("❌ API call failed:", response.status_code, response.text)

if __name__ == "__main__":
    process()
