"""Record HTTP destinations for bibliography URLs; not a semantic verifier."""
import argparse
import datetime
import json
import re
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--thesis", type=Path, default=Path("docs/thesis_final_2026_09_24"))
    args = parser.parse_args()
    bib = (args.thesis / "bibliography/references.bib").read_text()
    entries = re.split(r"(?m)^@", bib)[1:]
    rows = []
    for entry in entries:
        key = re.match(r"\w+\{([^,]+),", entry).group(1)
        match = re.search(r"url\s*=\s*\{([^}]+)\}", entry)
        if not match:
            raise ValueError(f"No URL for {key}")
        url = match.group(1)
        result = subprocess.run(
            ["curl", "-L", "--silent", "--show-error", "--max-time", "35",
             "-A", "Mozilla/5.0", "-o", "/dev/null",
             "-w", "%{http_code}\n%{url_effective}", url],
            capture_output=True, text=True,
        )
        lines = result.stdout.splitlines()
        rows.append({
            "key": key, "url": url,
            "http_status": lines[0] if lines else None,
            "final_url": lines[1] if len(lines) > 1 else None,
            "curl_exit_code": result.returncode,
            "error": result.stderr.strip() or None,
        })
        print(key, rows[-1]["http_status"], flush=True)
    output = {
        "checked_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "method": "curl GET with redirects; TLS verification enabled",
        "warning": "HTTP success does not prove bibliographic identity. See REFERENCE_AUDIT.md for title/metadata review. Access restrictions are not broken-link proof.",
        "references": rows,
    }
    path = args.thesis / "reference_link_check.json"
    path.write_text(json.dumps(output, indent=2) + "\n")
    print(path)


if __name__ == "__main__":
    main()
