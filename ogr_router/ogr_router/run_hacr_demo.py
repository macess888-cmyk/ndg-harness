from hacr.models import RouterInput
from hacr.router import HACRRouter

obj = RouterInput(
    object_id="example-001",
    object_type="publication",
    title="Example Convergence Note",
    scope={"declared": "external compatibility statement", "bounded": True},
    authorship={"primary_authors": ["Author A", "Author B"], "merged_authorship_claim": False},
    assumptions=[
        "Frameworks remain independent",
        "No baseline mutation is implied",
    ],
    invariant={"statement": "Compatibility does not collapse structural independence."},
    boundaries={"fail_closed_on": ["silent merger implication", "authorship drift", "implicit endorsement"]},
    reversibility={"last_safe_region": "pre-publication"},
    commitment_surface={"location": "public release"},
    transition={"mode": "around-baseline"},
    evidence={
        "observed": ["text of note", "declared scope language"],
        "inferred": ["public readers may assume integration"],
        "speculative": ["future downstream interpretation"],
    },
    cross_scale={"local": "pass", "system": "pass", "pressure": "provisional_pass"},
    separation_integrity={
        "compatibility_not_merger": True,
        "collaboration_not_authorship": True,
        "acknowledgment_not_endorsement": True,
    },
)

router = HACRRouter()
result = router.run(obj)

print("OBJECT:", result.object_id)
print("POSTURE:", result.posture.value)
print("SUMMARY:", result.summary_status)
print("CONSTRAINTS:", result.constraints)
for check in result.results:
    print(f"- {check.name}: {check.status.value} | {'; '.join(check.notes)}")