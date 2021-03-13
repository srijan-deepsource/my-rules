import json
import tempfile
import os
import subprocess

CODE_PATH = os.environ.get("CODE_PATH", "/code")


def prepare_result(issues):
    """Prepare the result for the DeepSource analyzer framework to publish."""
    return {
        "issues": issues,
        "metrics": [],
        "is_passed": True if issues else False,
        "errors": [],
        "extra_data": ""
    }


def publish_results(result):
    """Publish the analysis results."""
    # write results into a json file:
    res_file = tempfile.NamedTemporaryFile().name
    with open(res_file, "w") as fp:
        fp.write(json.dumps(result))

    # publish result via marvin:
    subprocess.run(["/toolbox/marvin", "--publish-report", res_file])


def get_issue_struct(issue_code, issue_txt, filepath, line, col):
    """Prepare issue structure for the given issue data."""
    return {
        "issue_code": issue_code,
        "issue_text": issue_txt,
        "location": {
            "path": filepath,
            "position": {
                "begin": {
                    "line": line,
                    "column": col
                },
                "end": {
                    "line": line,
                    "column": col
                }
            }
        }
    }

def analyze():
    issues = []
    for subdir, _, filenames in os.walk(CODE_PATH):
        for filename in filenames:
            filepath = os.path.join(subdir, filename)

            with open(filepath) as fp:
                lines = fp.readlines()

            for index, line in enumerate(lines):
                lno = index + 1
                if line.lower().startswith("hack"):
                    issues.append(
                        get_issue_struct(
                            "HREP-001",
                            f"Line {line} benins with the word `hack`. Don't do this please! Only the Hackster Boys are allowed to hack today.",
                            filepath,
                            lno,
                            0
                        )
                    )

    # Create result structure:
    result = prepare_result(issues)

    # Publish the result!
    publish_results(result)

if __name__ == "__main__":
    analyze()
