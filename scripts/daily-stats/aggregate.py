"""Publish daily page-request counts without visitor identifiers."""
import argparse
from collections import Counter
from datetime import date, datetime, timedelta
import fcntl
import gzip
import json
import os
from pathlib import Path
from zoneinfo import ZoneInfo


def signature(paths):
    return [(str(p), p.stat().st_ino) for p in paths]


def read_counts(log_dir):
    for _ in range(2):
        paths = sorted(log_dir.glob("me-bflame-daily.log*"))
        before = signature(paths)
        counts = Counter()
        for path in paths:
            reader = gzip.open if path.suffix == ".gz" else open
            with reader(path, "rt", encoding="utf-8") as handle:
                for line in handle:
                    value = line.strip()
                    if value:
                        date.fromisoformat(value)
                        counts[value] += 1
        if before == signature(sorted(log_dir.glob("me-bflame-daily.log*"))):
            return counts
    raise RuntimeError("Log rotation in progress; keep previous published data")


def atomic_json(path, data, mode):
    temporary = path.with_name(path.name + ".next")
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, mode)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False)
        handle.write("\n")
    os.chmod(temporary, mode)
    os.replace(temporary, path)


def update(log_dir, state_path, output, now=None):
    now = now or datetime.now(ZoneInfo("Asia/Taipei"))
    with open(state_path.with_suffix(".lock"), "a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        state = json.loads(state_path.read_text()) if state_path.exists() else {
            "started_at": now.isoformat(), "days": {}
        }
        counts = read_counts(log_dir)
        for day, count in counts.items():
            state["days"][day] = max(state["days"].get(day, 0), count)
        started = datetime.fromisoformat(state["started_at"]).date()
        days = []
        for offset in range(6, -1, -1):
            day = now.date() - timedelta(days=offset)
            days.append({"date": day.isoformat(),
                         "views": state["days"].get(day.isoformat(), 0) if day >= started else None,
                         "partial": day == started})
        payload = {"timezone": "Asia/Taipei", "updated_at": now.isoformat(),
                   "started_at": state["started_at"], "days": days}
        atomic_json(state_path, state, 0o600)
        atomic_json(output, payload, 0o644)
        return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--logs", type=Path, required=True)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    update(args.logs, args.state, args.output)
