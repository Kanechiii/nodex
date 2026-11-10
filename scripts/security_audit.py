"""Audit current Python source and Git history before public release."""

import ast
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY_DIRS = ("algorithms", "models", "structures", "tests")
SCAN_LIMIT = 512 * 1024

SECRET_RULES = (
    ("private key", re.compile(
        rb"-----BEGIN ((?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY)-----[ \t]*\r?\n"
        rb"(?:(?:[A-Za-z-]+:[^\r\n]*\r?\n)*\r?\n)?"
        rb"(?:[A-Za-z0-9+/=]{32,128}\r?\n)+-----END \1-----"
    )),
    ("AWS access key", re.compile(rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("GitHub token", re.compile(rb"\b(?:ghp_|gho_|ghu_|ghs_|ghr_)[A-Za-z0-9]{30,}\b")),
    ("GitHub fine-grained token", re.compile(rb"\bgithub_pat_[A-Za-z0-9_]{50,}\b")),
    ("OpenAI-style secret", re.compile(rb"\bsk-(?:proj-)?[A-Za-z0-9_-]{30,}\b")),
    ("credential assignment", re.compile(
        rb"(?im)^\s*(?:password|passwd|api_key|secret_key|access_token|auth_token)\s*[:=]\s*['\"][^'\"\r\n]{10,}['\"]"
    )),
)
SENSITIVE_NAMES = re.compile(
    r"(?i)(?:^|/)(?:\.env(?:\.[^/]*)?|id_rsa|id_ed25519|credentials\.json|"
    r"service.account\.json|[^/]+\.(?:pem|p12|pfx|key))$"
)
UNSAFE_CALLS = {"eval", "exec", "compile"}
UNSAFE_METHODS = {"system", "popen", "loads"}
RISK_IMPORTS = {"pickle", "marshal", "shelve"}
issues = []


def git(*args):
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout


def check_data(data, source):
    if len(data) > SCAN_LIMIT or b"\x00" in data:
        return
    for label, pattern in SECRET_RULES:
        for match in pattern.finditer(data):
            line = data.count(b"\n", 0, match.start()) + 1
            issues.append(f"{source}:{line}: possible {label} (value redacted)")


def check_history():
    entries = git("rev-list", "--objects", "--all").decode("utf-8", "replace")
    seen = set()
    for entry in entries.splitlines():
        parts = entry.split(" ", 1)
        if len(parts) != 2:
            continue
        obj_id, path = parts
        if SENSITIVE_NAMES.search(path):
            issues.append(f"History contains potentially sensitive filename: {path}")
        if obj_id in seen:
            continue
        seen.add(obj_id)
        if git("cat-file", "-t", obj_id).strip() != b"blob":
            continue
        size = int(git("cat-file", "-s", obj_id))
        if size > SCAN_LIMIT:
            continue
        check_data(git("cat-file", "-p", obj_id), f"Git blob {obj_id[:12]} ({path})")

    emails = set(git("log", "--all", "--format=%ae%n%ce").decode().splitlines())
    emails.discard("")
    if emails:
        print(f"NOTICE: {len(emails)} distinct commit author/committer email(s) in history.")
        print("Review those identities privately before changing visibility.")


def check_source():
    paths = [ROOT / "main.py"]
    for folder in PY_DIRS:
        paths.extend((ROOT / folder).rglob("*.py"))

    for path in paths:
        if not path.exists():
            continue
        data = path.read_bytes()
        check_data(data, str(path.relative_to(ROOT)))
        try:
            tree = ast.parse(data, filename=str(path))
        except SyntaxError as error:
            issues.append(f"{path.relative_to(ROOT)}: invalid Python syntax: {error}")
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] in RISK_IMPORTS:
                        issues.append(f"{path.name}:{node.lineno}: risky import {alias.name}")
            if isinstance(node, ast.ImportFrom) and node.module:
                if node.module.split(".")[0] in RISK_IMPORTS:
                    issues.append(f"{path.name}:{node.lineno}: risky import {node.module}")
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in UNSAFE_CALLS:
                    issues.append(f"{path.name}:{node.lineno}: review call to {node.func.id}")
                if isinstance(node.func, ast.Attribute):
                    name = node.func.attr
                    if name in UNSAFE_METHODS:
                        issues.append(f"{path.name}:{node.lineno}: review call to .{name}")
                    if name in ("run", "Popen", "call", "check_output", "check_call"):
                        if any(
                            kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True
                            for kw in node.keywords
                        ):
                            issues.append(f"{path.name}:{node.lineno}: shell=True")


def main():
    check_source()
    try:
        check_history()
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"ERROR: unable to audit complete Git history: {type(error).__name__}", file=sys.stderr)
        return 2

    if issues:
        print(f"Security audit found {len(issues)} potential issue(s):")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("Security heuristics passed: no matching secrets or flagged calls.")
    print("Passing does not replace GitHub secret scanning or a manual security review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
