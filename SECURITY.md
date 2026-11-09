# Pre-publication security review

The Nodex application is a local Python console simulation. It does not require network access, cloud credentials, or third-party packages.

## Automated checks

The [Security and Python checks](.github/workflows/security.yml) workflow runs on pull requests and pushes to `main`. It uses read-only repository permissions and pinned GitHub Actions commit SHAs. It tests Python 3.11 and 3.13, checks syntax, runs core/console tests and both traversal suites, and audits the tracked source plus reachable Git blob history for known secret patterns, suspicious credential filenames, and risky Python calls. The audit intentionally redacts any matching secret values.

To reproduce the checks locally:

```powershell
py -m compileall -q main.py algorithms models structures tests scripts
py -m unittest discover -s tests -p "test_*.py" -v
py -m unittest discover -s tests -p "*_check.py" -v
py scripts/security_audit.py
```

Run the script from a complete Git clone, not a downloaded ZIP. A shallow clone cannot expose all historical objects; on CI, checkout uses `fetch-depth: 0`.

## Required checks before changing visibility to public

1. Require an independent code review and a successful Security and Python checks workflow on the final `main` commit. GitHub branch protection is currently disabled; configure an appropriate ruleset before relying on checks.
2. Inspect **all Git history**, tags, PR branches, and releases for secrets, private files, personal information, and materials without permission to distribute. A pattern scanner can miss unknown formats and secrets not matched by its rules.
3. Review commit author/committer email addresses, contributor identities, issue/PR discussions, screenshots, and document metadata. GitHub exposes repository history on public repositories. The audit reports only the number of email addresses; review actual values privately.
4. Confirm there are no leaked access tokens, credentials, certificates or private keys. If one is found, revoke/rotate it **before** any history rewrite. Deleting a file in a later commit does not remove prior versions.
5. Enable GitHub's available secret scanning, push protection, and dependency/security features as supported by the repository/account. Review security alerts in GitHub's Security tab.
6. Audit linked content, dependencies, and any pending local changes not yet pushed. Check third-party code licenses and verify the project can be redistributed.
7. Re-run all checks on the final merged commit and only then decide whether to change visibility. This PR deliberately does not change repository settings.

## Limits

The scanner uses signatures and AST heuristics; a pass is **not** proof that the project is vulnerability-free. In particular, it does not test package vulnerabilities, history held only in unreachable objects, external services, CI secrets, collaborators' local files, or information posted outside tracked source files.
