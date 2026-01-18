import json
from src.provenance import generate_profile_write_out

def main():
    profile = generate_profile_write_out()
    print("Profile generated. Summary:")
    print(f"- tasks: {profile.get('n_tasks')}")
    uniq = profile.get("uniqueness", {})
    print(f"- uniqueness avg/min/max: {uniq.get('avg')}/{uniq.get('min')}/{uniq.get('max')}")
    print("- top_signatures:")
    for s in profile.get("top_signatures", []):
        print(f"  - {s['sig']}: {s['count']}")
    with open("data/profile_summary.txt", "w", encoding="utf-8") as f:
        f.write(f"tasks: {profile.get('n_tasks')}\n")
        f.write(f"uniqueness avg/min/max: {uniq.get('avg')}/{uniq.get('min')}/{uniq.get('max')}\n")
        for s in profile.get("top_signatures", []):
            f.write(f"{s['sig']}: {s['count']}\n")

if __name__ == "__main__":
    main()
