from __future__ import annotations

from typing import List

import yaml

from hacr.models import CheckResult, Posture, RouterInput, RouterOutput, Status


def load_router_input_from_yaml(path: str) -> RouterInput:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return RouterInput(**data)


class HACRRouter:
    def run(self, obj: RouterInput) -> RouterOutput:
        results = [
            self.identity_check(obj),
            self.invariant_check(obj),
            self.gfb_check(obj),
            self.reversibility_check(obj),
            self.halt_authority_check(obj),
            self.ogr_transition_check(obj),
            self.mdis_check(obj),
            self.cross_scale_check(obj),
            self.separation_check(obj),
        ]
        posture, constraints = self.decide(results, obj)
        summary = self._summary_status(results)
        return RouterOutput(
            object_id=obj.object_id,
            posture=posture,
            summary_status=summary,
            results=results,
            constraints=constraints,
        )

    def identity_check(self, obj: RouterInput) -> CheckResult:
        notes: List[str] = []
        if not obj.scope.get("declared"):
            notes.append("Scope is not declared.")
        if not obj.authorship.get("primary_authors"):
            notes.append("Primary authorship is not declared.")
        status = Status.PASS if not notes else Status.HOLD
        return CheckResult("identity", status, notes)

    def invariant_check(self, obj: RouterInput) -> CheckResult:
        statement = obj.invariant.get("statement", "")
        if not statement.strip():
            return CheckResult("invariant", Status.HOLD, ["Invariant is missing."])
        return CheckResult("invariant", Status.PASS, ["Invariant stated."])

    def gfb_check(self, obj: RouterInput) -> CheckResult:
        fail_closed_on = obj.boundaries.get("fail_closed_on", [])
        if not fail_closed_on:
            return CheckResult("gfb", Status.HOLD, ["No fail-closed conditions declared."])
        return CheckResult("gfb", Status.PASS, ["Fail-closed conditions declared."])

    def reversibility_check(self, obj: RouterInput) -> CheckResult:
        region = obj.reversibility.get("last_safe_region")
        if not region:
            return CheckResult("reversibility", Status.FAIL, ["No last safe region declared."])
        return CheckResult("reversibility", Status.PASS, [f"Last safe region: {region}"])

    def halt_authority_check(self, obj: RouterInput) -> CheckResult:
        location = obj.commitment_surface.get("location")
        if not location:
            return CheckResult("halt_authority", Status.HOLD, ["Commitment surface not identified."])
        return CheckResult("halt_authority", Status.PASS, [f"Commitment surface: {location}"])

    def ogr_transition_check(self, obj: RouterInput) -> CheckResult:
        mode = obj.transition.get("mode")
        if mode == "around-baseline":
            return CheckResult("ogr_transition", Status.PASS, ["Transition remains around baseline."])
        if mode == "baseline-mutation":
            return CheckResult("ogr_transition", Status.FAIL, ["Baseline mutation detected."])
        return CheckResult("ogr_transition", Status.HOLD, ["Transition mode is unclear."])

    def mdis_check(self, obj: RouterInput) -> CheckResult:
        observed = obj.evidence.get("observed", [])
        inferred = obj.evidence.get("inferred", [])
        speculative = obj.evidence.get("speculative", [])
        if observed is None or inferred is None or speculative is None:
            return CheckResult("mdis", Status.HOLD, ["Evidence layers are incomplete."])
        return CheckResult(
            "mdis",
            Status.PASS,
            [
                f"Observed: {len(observed)}",
                f"Inferred: {len(inferred)}",
                f"Speculative: {len(speculative)}",
            ],
        )

    def cross_scale_check(self, obj: RouterInput) -> CheckResult:
        local = obj.cross_scale.get("local")
        system = obj.cross_scale.get("system")
        pressure = obj.cross_scale.get("pressure")
        if not all([local, system, pressure]):
            return CheckResult("cross_scale", Status.PROVISIONAL, ["Cross-scale fields incomplete."])
        return CheckResult("cross_scale", Status.PASS, [f"local={local}, system={system}, pressure={pressure}"])

    def separation_check(self, obj: RouterInput) -> CheckResult:
        fields = obj.separation_integrity
        required = [
            "compatibility_not_merger",
            "collaboration_not_authorship",
            "acknowledgment_not_endorsement",
        ]
        failed = [k for k in required if not fields.get(k, False)]
        if failed:
            return CheckResult("separation_integrity", Status.FAIL, [f"Boundary failure: {', '.join(failed)}"])
        return CheckResult("separation_integrity", Status.PASS, ["Separation integrity intact."])

    def decide(self, results: List[CheckResult], obj: RouterInput) -> tuple[Posture, List[str]]:
        constraints: List[str] = []
        statuses = {r.name: r.status for r in results}

        if statuses.get("reversibility") == Status.FAIL:
            return Posture.REJECT, ["No reversible region visible."]
        if statuses.get("ogr_transition") == Status.FAIL:
            return Posture.ROLLBACK, ["Baseline mutation requires reopening invariants."]
        if statuses.get("separation_integrity") == Status.FAIL:
            return Posture.COMPATIBLE_BUT_INDEPENDENT, ["Restore authorship and merger boundaries."]
        if Status.HOLD in statuses.values():
            constraints.append("Complete missing fields before commitment.")
            return Posture.HOLD, constraints
        if statuses.get("cross_scale") == Status.PROVISIONAL:
            return Posture.SUPPORT, ["Support is provisional pending pressure validation."]
        return Posture.SUPPORT, ["Maintain explicit boundaries."]

    def _summary_status(self, results: List[CheckResult]) -> str:
        if any(r.status == Status.FAIL for r in results):
            return "failure_detected"
        if any(r.status == Status.HOLD for r in results):
            return "incomplete"
        if any(r.status == Status.PROVISIONAL for r in results):
            return "provisional"
        return "admissible"