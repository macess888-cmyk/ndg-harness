from hacr.router import HACRRouter, load_router_input_from_yaml

obj = load_router_input_from_yaml("hacr/examples/convergence_note.yaml")
router = HACRRouter()
result = router.run(obj)

print("OBJECT:", result.object_id)
print("POSTURE:", result.posture.value)
print("SUMMARY:", result.summary_status)
print("CONSTRAINTS:", result.constraints)
for check in result.results:
    print(f"- {check.name}: {check.status.value} | {'; '.join(check.notes)}")