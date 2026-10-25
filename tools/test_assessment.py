"""Behavior checks for the assessment data contract."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest
import sys
sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "elementary-competency-assessment-local"
spec = importlib.util.spec_from_file_location("builder", SKILL / "scripts/build_assessment.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
FIXTURE = SKILL / "examples/smoke-assessment.json"

class MasterValidation(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    def rejected(self):
        with self.assertRaises(ValueError):
            builder.validate(self.data, FIXTURE.parent)
    def test_valid_master(self):
        builder.validate(self.data, FIXTURE.parent)
    def test_total_score_mismatch(self):
        self.data["total_score"] += 1
        self.rejected()
    def test_missing_option_explanation(self):
        del self.data["questions"][0]["option_explanations"]["D"]
        self.rejected()
    def test_rubric_score_mismatch(self):
        self.data["questions"][1]["rubric"][0]["points"] += 1
        self.rejected()
    def test_partial_credit_cannot_be_full_credit(self):
        self.data["questions"][1]["partial_credit_examples"][0]["points"] = 6
        self.rejected()
    def test_missing_blueprint_question(self):
        self.data["blueprint"].pop()
        self.rejected()
    def test_question_order_mismatch(self):
        self.data["questions"][0]["id"] = 3
        self.rejected()
    def test_missing_image(self):
        self.data["materials"].append({"type":"image","path":"missing-test.png","caption":"測試圖"})
        self.rejected()
    def test_group_cannot_be_split_by_other_question(self):
        self.data["questions"][1]["group"] = "其他題組"
        extra = copy.deepcopy(self.data["questions"][0])
        extra["id"] = 3
        self.data["questions"].append(extra)
        self.rejected()
    def test_estimated_time_mismatch(self):
        self.data["blueprint"][0]["minutes"] = 10
        self.rejected()
    def test_official_source_needs_real_url(self):
        self.data["sources"][0]["kind"] = "official"
        self.rejected()

if __name__ == "__main__":
    unittest.main(verbosity=2)
