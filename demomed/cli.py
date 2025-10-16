import os, json, argparse
from .client import DemoMedClient
from .alerts import build_alert_lists
from .scoring import total_score

def main():
    ap = argparse.ArgumentParser(description="DemoMed assessment CLI")
    ap.add_argument("--limit", type=int, default=10, help="page size (<=20)")
    ap.add_argument("--dry-run", action="store_true", help="print payload only")
    ap.add_argument("--submit", action="store_true", help="submit payload to API")
    args = ap.parse_args()

    client = DemoMedClient()

    print("🔍 Fetching patients...")
    patients = client.list_patients(limit=min(max(args.limit,1),20))
    print(f"✅ Retrieved {len(patients)} patients.")

    payload = build_alert_lists(patients)

    # optional local CSV/export
    try:
        import csv
        rows = [
            {
                "patient_id": p.get("patient_id"),
                "name": p.get("name"),
                "total_risk": total_score(p),
                "temperature": p.get("temperature"),
            } for p in patients
        ]
        with open("patient_risk_summary.csv","w",newline="") as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
        print("🗂️  Saved patient_risk_summary.csv")
    except Exception as e:
        print("CSV save skipped:", e)

    print("\n📦 Payload:")
    print(json.dumps(payload, indent=2))

    if args.submit:
        if args.dry_run:
            print("\n⚠️  Dry-run enabled: not submitting.")
        else:
            print("\n📤 Submitting...")
            resp = client.submit(payload)
            print("🧾 Response:", json.dumps(resp, indent=2))
    else:
        print("\nℹ️  Not submitting (use --submit to send).")

if __name__ == "__main__":
    main()
