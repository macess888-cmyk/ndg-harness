from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from hacr.router import HACRRouter, load_router_input_from_yaml


def main() -> None:
    parser = argparse.ArgumentParser(prog="hacr")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check", help="Check a HACR YAML object")
    check_parser.add_argument("path", help="Path to YAML file")
    check_parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON output",
    )
    check_parser.add_argument(
        "--out",
        help="Optional file path to write JSON output",
    )

    args = parser.parse_args()

    if args.command == "check":
        obj = load_router_input_from_yaml(args.path)
        router = HACRRouter()
        result = router.run(obj)

        if args.json:
            result_dict = asdict(result)
            json_text = json.dumps(result_dict, indent=2)

            if args.out:
                with open(args.out, "w", encoding="utf-8") as f:
                    f.write(json_text)
                print(f"Wrote JSON report to {args.out}")
            else:
                print(json_text)
            return

        print("OBJECT:", result.object_id)
        print("POSTURE:", result.posture.value)
        print("SUMMARY:", result.summary_status)
        print("CONSTRAINTS:", result.constraints)
        for check in result.results:
            print(f"- {check.name}: {check.status.value} | {'; '.join(check.notes)}")


if __name__ == "__main__":
    main()