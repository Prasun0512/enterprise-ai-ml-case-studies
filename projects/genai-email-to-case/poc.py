from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.case_study_pocs import POC_RUNNERS


PROJECT = "genai-email-to-case"


def run_demo() -> dict:
    return asdict(POC_RUNNERS[PROJECT]())


if __name__ == "__main__":
    print(json.dumps(run_demo(), indent=2))
