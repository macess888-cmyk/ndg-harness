import json
import subprocess
import sys
from pathlib import Path

from hacr.models import Posture, RouterInput
from hacr.router import HACRRouter, load_router_input_from_yaml


def make_example() -> RouterInput:
    return RouterInput(
        object_id="example-001",
        object_type="publication",
        title="Example Convergence Note",
        scope={"declared": "external compatibility statement", "bounded": True},
        authorship={
            "primary_authors": ["Author A", "Author B"],
            "merged_authorship_claim": False,
        },
        assumptions=[
            "Frameworks remain independent",
            "No baseline mutation is implied",
        ],
        invariant={
            "statement": "Compatibility does not collapse structural independence."
        },
        boundaries={
            "fail_closed_on": [
                "silent merger implication",
                "authorship drift",
                "implicit endorsement",
            ]
        },
        reversibility={"last_safe_region": "pre-publication"},
        commitment_surface={"location": "public release"},
        transition={"mode": "around-baseline"},
        evidence={
            "observed": ["text of note", "declared scope language"],
            "inferred": ["public readers may assume integration"],
            "speculative": ["future downstream interpretation"],
        },
        cross_scale={
            "local": "pass",
            "system": "pass",
            "pressure": "provisional_pass",
        },
        separation_integrity={
            "compatibility_not_merger": True,
            "collaboration_not_authorship": True,
            "acknowledgment_not_endorsement": True,
        },
    )


def test_router_support_case():
    router = HACRRouter()
    result = router.run(make_example())
    assert result.posture == Posture.SUPPORT


def test_yaml_loader():
    obj = load_router_input_from_yaml("hacr/examples/convergence_note.yaml")
    router = HACRRouter()
    result = router.run(obj)
    assert result.posture == Posture.SUPPORT


def test_cli_check():
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "hacr.cli",
            "check",
            "hacr/examples/convergence_note.yaml",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "POSTURE: support" in completed.stdout


def test_cli_json_output():
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "hacr.cli",
            "check",
            "hacr/examples/convergence_note.yaml",
            "--json",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(completed.stdout)
    assert data["object_id"] == "example-001"
    assert data["posture"] == "support"


def test_cli_json_file_output(tmp_path: Path):
    out_file = tmp_path / "report.json"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "hacr.cli",
            "check",
            "hacr/examples/convergence_note.yaml",
            "--json",
            "--out",
            str(out_file),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    assert out_file.exists()
    data = json.loads(out_file.read_text(encoding="utf-8"))
    assert data["object_id"] == "example-001"
    assert data["posture"] == "support"
    assert "Wrote JSON report" in completed.stdout