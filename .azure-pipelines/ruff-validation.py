from __future__ import annotations

import subprocess
import json

failures = 0
try:
    output = subprocess.run(
        ["ruff", "check", "--exit-zero", "--output-format", "json", "."],
        capture_output=True,
        check=True,
        timeout=300,
    )
except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
    print(
        "##vso[task.logissue type=error;]ruff validation failed with",
        str(e.__class__.__name__),
    )
    print(e.stdout)
    print(e.stderr)
    print("##vso[task.complete result=Failed;]ruff validation failed")
    exit()

results = json.loads(output.stdout)

for violation in results:
    # filename, lineno, column, error = line.split(":", maxsplit=3)
    # errcode, error = error.strip().split(" ", maxsplit=1)
    # filename = os.path.normpath(filename)
    failures += 1
    print(
        f"##vso[task.logissue type=error;sourcepath={violation['filename']};"
        f"linenumber={violation['location']['row']};columnnumber={violation['location']['column']};code={violation['code']};]"
        + violation["message"]
    )

if failures:
    print(f"##vso[task.logissue type=warning]Found {failures} ruff violation(s)")
    print(f"##vso[task.complete result=Failed;]Found {failures} ruff violation(s)")
