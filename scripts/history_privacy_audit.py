"""Read-only audit of historical bytecode and commit identities."""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_SIZE = 5 * 1024 * 1024
EMAIL = re.compile(rb"(?i)[\w.+-]+@[\w.-]+\.[a-z]{2,}")
PATHS = (
    re.compile(rb"(?i)\b[A-Z]:[\\/](?:Users|Documents and Settings)[\\/][^\\/\x00\r\n]{1,100}"),
    re.compile(rb"(?i)/(?:home|Users)/[^/\x00\r\n]{1,100}"),
)
SECRETS = (
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    re.compile(rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    re.compile(rb"\b(?:ghp_|gho_|ghu_|ghs_|ghr_)[A-Za-z0-9]{30,}\b"),
    re.compile(rb"\bgithub_pat_[A-Za-z0-9_]{50,}\b"),
    re.compile(rb"\bsk-(?:proj-)?[A-Za-z0-9_-]{30,}\b"),
    re.compile(rb'''(?im)^\s*(?:password|passwd|api_key|secret_key|access_token|auth_token)\s*[:=]\s*['"][^'"\r\n]{10,}['"]'''),
)


def git(*args):
    return subprocess.run(
        ["git", *args], cwd=ROOT, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=True,
    ).stdout


def classify(email):
    value = email.strip().lower()
    if value == "noreply@github.com" or value.endswith("@users.noreply.github.com"):
        return "GitHub no-reply"
    return "other email"


def scan_blob(data):
    return {
        "secrets": sum(len(rule.findall(data)) for rule in SECRETS),
        "emails": len(EMAIL.findall(data)),
        "paths": sum(len(rule.findall(data)) for rule in PATHS),
    }


def get_blobs():
    trees = set(git("log", "--all", "--format=%T").splitlines())
    found = {}
    for tree in sorted(trees):
        entries = git("ls-tree", "-r", "-z", tree.decode("ascii"))
        for entry in entries.split(b"\x00"):
            if not entry:
                continue
            meta, separator, path = entry.partition(b"\t")
            if not separator or not path.lower().endswith(b".pyc"):
                continue
            parts = meta.split()
            if len(parts) != 3 or parts[1] != b"blob":
                continue
            sha = parts[2].decode("ascii")
            found.setdefault(sha, path.decode("utf-8", "replace"))
    return sorted(found.items())


def audit():
    raw = git("log", "--all", "--format=%ae%n%ce")
    emails = set(raw.decode("utf-8", "replace").splitlines())
    emails.discard("")
    exposed = sum(classify(email) == "other email" for email in emails)
    print(f"Commit identities: {len(emails)} distinct address(es), "
          f"{exposed} non-no-reply (values withheld).")

    blobs = get_blobs()
    print(f"Historical Python bytecode objects: {len(blobs)}.")
    findings = 0
    for sha, path in blobs:
        if git("cat-file", "-t", sha).strip() != b"blob":
            print(f"UNSCANNED bytecode object {sha[:12]}: not a blob")
            findings += 1
            continue
        size = int(git("cat-file", "-s", sha))
        if size > MAX_SIZE:
            print(f"UNSCANNED bytecode object {sha[:12]}: exceeds size limit")
            findings += 1
            continue
        report = scan_blob(git("cat-file", "blob", sha))
        if any(report.values()):
            print(f"REVIEW bytecode object {sha[:12]}: possible secrets={report['secrets']}, "
                  f"email-like strings={report['emails']}, "
                  f"local user paths={report['paths']} (values withheld)")
            findings += 1
    if findings:
        print("Review flagged historical objects privately before publication.")
        return 1
    print("No matching indicators in historical Python bytecode.")
    print("Heuristic scan only; this does not prove the history is safe.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(audit())
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"Unable to audit Git history: {type(error).__name__}", file=sys.stderr)
        sys.exit(2)
