from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

from src.case_study_pocs import POC_RUNNERS


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class CaseStudyPocTests(unittest.TestCase):
    def test_all_project_folders_have_runnable_pocs(self) -> None:
        project_dirs = sorted(path for path in (PROJECT_ROOT / "projects").iterdir() if path.is_dir())
        self.assertEqual(len(project_dirs), len(POC_RUNNERS))

        for project_dir in project_dirs:
            poc_path = project_dir / "poc.py"
            self.assertTrue(poc_path.exists(), f"{project_dir.name} is missing poc.py")

            spec = importlib.util.spec_from_file_location(f"{project_dir.name}_poc", poc_path)
            self.assertIsNotNone(spec)
            self.assertIsNotNone(spec.loader)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            result = module.run_demo()
            self.assertEqual(result["project"], project_dir.name)
            self.assertTrue(result["status"])
            self.assertTrue(result["payload"])
            self.assertTrue(result["audit"])


if __name__ == "__main__":
    unittest.main()
