"""Silent local watchdog: no AI calls; at most two evaluator resumes."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/evaluation/source_preference_trial_2026_09_22"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pid", type=int, required=True)
    args = parser.parse_args()
    pid, child, retries = args.pid, None, 0
    # Exclusive lock prevents duplicate watchdogs from starting duplicate evaluations.
    import fcntl
    with (OUT / "watchdog.lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        while True:
            try:
                rows = json.loads((OUT / "results.json").read_text())["rows"]
                jobs = json.loads((OUT / "plan.json").read_text())["jobs"]
                completed = {(r["id"], r["variant"]) for r in rows}
                if all((j["id"], j["variant"]) in completed for j in jobs):
                    print("Complete; watchdog stopped.", flush=True)
                    return
            except FileNotFoundError:
                pass
            if child is not None:
                alive = child.poll() is None
            else:
                try:
                    os.kill(pid, 0)
                    alive = True
                except ProcessLookupError:
                    alive = False
            if not alive:
                if retries >= 2:
                    print("Retry limit reached; stopped. Inspect run.log.", flush=True)
                    return
                retries += 1
                print(f"Evaluator stopped; resume attempt {retries}/2.", flush=True)
                with (OUT / "run.log").open("a") as log:
                    child = subprocess.Popen([sys.executable, "-u", "scripts/test_source_preference.py", "--resume"],
                                             cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
                pid = child.pid
            time.sleep(120)


if __name__ == "__main__":
    main()
