"""Exercise preparation in disposable repositories, never in a simulation run."""

import csv
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "prepare_runs.py"
FNN_RUN = "alanine/run_biased_nn/DeepTICA/dataset1/0"
GNN_RUN = "alanine/run_biased_gnn/SelfTICA/T2_dataset/3"


class PrepareRunsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="selftica-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        if SCRIPT.is_file():
            self.put("scripts/prepare_runs.py", SCRIPT.read_bytes())
        self.put("alanine/common/ala2.tpr", b"original\x00TPR\xff")
        self.put("tri-well/common/md_potential", b"potential coefficients\n")
        self.put("alanine/plumed-descriptors.dat", b"d1: DISTANCE ATOMS=2,5\n")
        self.put("plumed/PytorchGNN.cpp", b"// custom interface\n")
        self.put("alanine/data/plumed_topo.pdb", b"structure\n")
        self.put("alanine/models/std/DeepTICA/FNN/dataset1/model_0.pt", b"fnn model")
        self.put("alanine/models/std/SelfTICA/GNN/dataset2/model_3.pt", b"gnn model")
        self.put("alanine/templates/fnn.dat.in", (
            "INCLUDE FILE=../../../../plumed-descriptors.dat\n"
            "deep: PYTORCH_MODEL FILE=@MODEL_PATH@ ARG=d1\n"
            "PRINT FILE=COLVAR ARG=*\n"
        ).encode())
        self.put("alanine/templates/gnn.dat.in", (
            "LOAD FILE=../../../../../plumed/PytorchGNN.cpp\n"
            "MOLINFO STRUCTURE=../../../../data/plumed_topo.pdb\n"
            "PYTORCH_GNN MODEL=@MODEL_PATH@\nPRINT FILE=COLVAR ARG=*\n"
        ).encode())
        self.shared = {"version": 1, "files": [{
            "source": "tri-well/common/md_potential",
            "targets": ["tri-well/run_unbiased/1.0kbt/md_potential"],
        }]}
        self.write_shared()
        with (self.root / "alanine/experiments.csv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream)
            writer.writerow(["run_dir", "architecture", "method", "dataset", "replica", "model"])
            writer.writerow([FNN_RUN, "FNN", "DeepTICA", "dataset1", "0",
                             "alanine/models/std/DeepTICA/FNN/dataset1/model_0.pt"])
            writer.writerow([GNN_RUN, "GNN", "SelfTICA", "dataset2", "3",
                             "alanine/models/std/SelfTICA/GNN/dataset2/model_3.pt"])

    def put(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    def write_shared(self):
        self.put("scripts/shared-inputs.json", json.dumps(self.shared).encode())

    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(self.root / "scripts/prepare_runs.py"), *args],
                              cwd=self.root, capture_output=True, text=True)

    def assert_success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_selected_experiment_preserves_model_and_binary_input(self):
        self.assert_success(self.run_cli("--run", FNN_RUN))
        self.assertEqual((self.root / FNN_RUN / "plumed.dat").read_text(),
                         "INCLUDE FILE=../../../../plumed-descriptors.dat\n"
                         "deep: PYTORCH_MODEL FILE=../../../../models/std/DeepTICA/FNN/dataset1/model_0.pt ARG=d1\n"
                         "PRINT FILE=COLVAR ARG=*\n")
        self.assertEqual((self.root / FNN_RUN / "ala2.tpr").read_bytes(), b"original\x00TPR\xff")
        self.assertFalse((self.root / GNN_RUN).exists())
        self.assertFalse((self.root / "tri-well/run_unbiased").exists())

    def test_all_prepares_both_architectures_and_shared_inputs(self):
        self.assert_success(self.run_cli("--all"))
        self.assertIn("MODEL=../../../../models/std/SelfTICA/GNN/dataset2/model_3.pt",
                      (self.root / GNN_RUN / "plumed.dat").read_text())
        self.assertEqual((self.root / "tri-well/run_unbiased/1.0kbt/md_potential").read_bytes(),
                         b"potential coefficients\n")

    def test_repeat_preparation_preserves_inputs_and_simulation_outputs(self):
        self.assert_success(self.run_cli("--run", FNN_RUN))
        config = self.root / FNN_RUN / "plumed.dat"
        before = config.stat().st_mtime_ns
        self.put(FNN_RUN + "/COLVAR", b"precious trajectory\n")
        self.assert_success(self.run_cli("--run", FNN_RUN))
        self.assertEqual(config.stat().st_mtime_ns, before)
        self.assertEqual((self.root / FNN_RUN / "COLVAR").read_bytes(), b"precious trajectory\n")

    def test_conflict_prevents_all_selected_writes(self):
        self.put(FNN_RUN + "/plumed.dat", b"user-edited parameters\n")
        result = self.run_cli("--all")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("plumed.dat", result.stderr)
        self.assertEqual((self.root / FNN_RUN / "plumed.dat").read_bytes(), b"user-edited parameters\n")
        self.assertFalse((self.root / FNN_RUN / "ala2.tpr").exists())
        self.assertFalse((self.root / GNN_RUN).exists())

    def test_check_and_list_do_not_materialize_inputs(self):
        self.assert_success(self.run_cli("--check"))
        result = self.run_cli("--list")
        self.assert_success(result)
        self.assertIn(FNN_RUN, result.stdout.splitlines())
        self.assertIn("tri-well/run_unbiased/1.0kbt", result.stdout.splitlines())
        self.assertFalse((self.root / FNN_RUN).exists())

    def test_missing_model_prevents_preparation(self):
        (self.root / "alanine/models/std/SelfTICA/GNN/dataset2/model_3.pt").unlink()
        result = self.run_cli("--all")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("model_3.pt", result.stderr)
        self.assertFalse((self.root / FNN_RUN).exists())

    def test_unknown_run_is_rejected_without_writes(self):
        result = self.run_cli("--run", "alanine/misspelled")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("alanine/misspelled", result.stderr)
        self.assertFalse((self.root / "alanine/misspelled").exists())

    def test_manifest_cannot_write_outside_repository(self):
        self.shared["files"][0]["targets"] = ["../escaped-input"]
        self.write_shared()
        result = self.run_cli("--all")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("escaped-input", result.stderr)
        self.assertFalse((self.root / FNN_RUN).exists())

    def test_missing_template_dependency_is_reported(self):
        (self.root / "plumed/PytorchGNN.cpp").unlink()
        result = self.run_cli("--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("PytorchGNN.cpp", result.stderr)

    def test_template_requires_exactly_one_model_placeholder(self):
        self.put("alanine/templates/fnn.dat.in", b"PYTORCH_MODEL FILE=wrong-model.pt\n")
        result = self.run_cli("--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("MODEL_PATH", result.stderr)


if __name__ == "__main__":
    unittest.main()
